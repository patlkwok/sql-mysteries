import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

from sql_mystery_agent import MysteryDatabase, run_agent


class ScriptedClient:
    """A deterministic Responses API stand-in for testing the tool loop."""

    def __init__(self) -> None:
        self.step = 0
        self.observed_outputs: List[Dict[str, Any]] = []

    def create(
        self,
        input_data: Any,
        _tools: List[Dict[str, Any]],
        previous_response_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if previous_response_id:
            self.observed_outputs.extend(input_data)

        scripted = [
            {
                "id": "response-1",
                "output": [
                    {
                        "type": "function_call",
                        "name": "query_database",
                        "call_id": "call-1",
                        "arguments": json.dumps(
                            {
                                "sql": (
                                    "SELECT description FROM crime_scene_report "
                                    "WHERE date = 20180115 AND type = 'murder' "
                                    "AND city = 'SQL City'"
                                )
                            }
                        ),
                    }
                ],
            },
            {
                "id": "response-2",
                "output": [
                    {
                        "type": "function_call",
                        "name": "submit_solution",
                        "call_id": "call-2",
                        "arguments": json.dumps({"name": "Investigator One"}),
                    }
                ],
            },
            {
                "id": "response-3",
                "output": [
                    {
                        "type": "function_call",
                        "name": "submit_solution",
                        "call_id": "call-3",
                        "arguments": json.dumps({"name": "Mastermind Two"}),
                    }
                ],
            },
            {
                "id": "response-4",
                "output_text": "The database confirms both stages.",
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": "The database confirms both stages.",
                            }
                        ],
                    }
                ],
            },
        ]
        response = scripted[self.step]
        self.step += 1
        return response


class MysteryDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "fixture.db"
        connection = sqlite3.connect(str(self.database_path))
        connection.executescript(
            """
            CREATE TABLE person (id INTEGER PRIMARY KEY, name TEXT);
            INSERT INTO person (name) VALUES ('Investigator One'), ('Mastermind Two');

            CREATE TABLE crime_scene_report (
                date INTEGER,
                type TEXT,
                city TEXT,
                description TEXT
            );
            INSERT INTO crime_scene_report VALUES (
                20180115,
                'murder',
                'SQL City',
                'Synthetic evidence for the tool-loop test.'
            );

            CREATE TABLE solution (user INTEGER, value TEXT);
            CREATE TRIGGER check_solution AFTER INSERT ON solution
            BEGIN
                DELETE FROM solution;
                INSERT INTO solution VALUES (
                    0,
                    CASE
                        WHEN new.value = 'Investigator One'
                            THEN 'Congrats, you found the murderer!'
                        WHEN new.value = 'Mastermind Two'
                            THEN 'Congrats, you found the brains behind the murder!'
                        ELSE 'That is not the right person.'
                    END
                );
            END;
            """
        )
        connection.close()
        self.database = MysteryDatabase(self.database_path)

    def tearDown(self) -> None:
        self.database.close()
        self.temp_directory.cleanup()

    def test_query_is_read_only(self) -> None:
        result = json.loads(self.database.query("DELETE FROM person"))
        self.assertIn("error", result)

        count = json.loads(self.database.query("SELECT count(*) AS n FROM person"))
        self.assertGreater(count["rows"][0][0], 0)

    def test_solution_checks_do_not_modify_source_database(self) -> None:
        before = self.database_path.read_bytes()
        self.database.submit_solution("Investigator One")
        self.database.submit_solution("Mastermind Two")
        after = self.database_path.read_bytes()

        self.assertTrue(self.database.solved)
        self.assertEqual(before, after)

    def test_agent_requires_both_database_verdicts(self) -> None:
        client = ScriptedClient()
        answer = run_agent(self.database, client, verbose=False)

        self.assertTrue(self.database.stage_one_passed)
        self.assertTrue(self.database.stage_two_passed)
        self.assertEqual(answer, "The database confirms both stages.")
        self.assertEqual(len(client.observed_outputs), 3)


if __name__ == "__main__":
    unittest.main()
