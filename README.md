# SQL Murder Mystery

![Illustration of a detective looking at evidence](174092-clue-illustration.png)

There's been a Murder in SQL City! The SQL Murder Mystery is designed to be both a self-directed lesson to learn SQL concepts and commands and a fun game for experienced SQL users to solve an intriguing crime.

If you just want to solve the mystery, go to [mystery.knightlab.com](https://mystery.knightlab.com). If you're new to SQL, you may want to start at [our walkthrough](https://mystery.knightlab.com/walkthrough.html). It won't teach you everything about SQL, but it should teach you all that you need to solve the mystery.  

## What Else is Here?

Before we built the web-based version, we designed this for people to download and solve on their own computer. If you're interested in that, read on.

## What you need to solve on your own computer

* **sql-murder-mystery.db**: This SQLite database file contains all the data that you will be working with.
* **prompt**: Depending on your experience level with SQL, find the prompt in either the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file or the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file.
* **[reference](https://github.com/NUKnightLab/sql-mysteries/blob/master/reference.pdf)**: This is a crash course on SQL concepts and commands.
* **a SQLite environment of your choice**: For beginners, we recommend using [SQLiteStudio](https://sqlitestudio.pl/), which is a good graphical interface to use to inspect your data and write queries.

## Getting Started
* **For SQL beginners**: start with the reference, read the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file, then get started by [installing SQLiteStudio and loading the db file](https://github.com/NUKnightLab/sql-mysteries/blob/master/sqlite_studio.pdf). If you get stuck at any point, feel free to refer back to the reference, or file a [GitHub issue](https://github.com/NUKnightLab/sql-mysteries/issues) so we can know where our instructions need to be improved.

* **For experienced SQL users**: read the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file, then download the sql-murder-mystery.db file and use a SQL environment of your choice to solve the mystery. You can use the reference to refresh your memory of SQL. Try to complete the activity all within your SQL environment (without writing down notes)!


## Checking the Solution
Write the following queries in your SQL environment to check whether you've found the right murderer:

```SQL
INSERT INTO solution VALUES (1, "Insert the name of the person you found here");

SELECT value FROM solution;
```

## Letting an AI Agent Play

`sql_mystery_agent.py` is a command-line, tool-using agent that starts with only the public crime prompt. It can run read-only SQL against an in-memory copy of the game database and submit suspects to the database's original solution checker. It stops successfully only after the checker confirms both stages.

It uses Python's standard library and the OpenAI Responses API, so it has no additional package dependencies. Python 3.8 or newer is required.

In PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
py sql_mystery_agent.py
```

On macOS or Linux with Bash, Zsh, or a compatible shell:

```bash
export OPENAI_API_KEY="your-api-key"
python3 sql_mystery_agent.py
```

The agent is cross-platform and uses only Python's standard library. On every platform it requires Python 3.8 or newer, internet access to `api.openai.com`, and an OpenAI API key with API billing enabled. The examples below use PowerShell; on macOS or Linux, replace `py` with `python3`, remove PowerShell's line-continuation backticks, and use `\` when splitting a command across lines.

### Agent options

The agent supports the following command-line flags:

| Flag | Default | Description |
| --- | --- | --- |
| `--database PATH` | `sql-murder-mystery.db` next to the script | Use a different SQL Murder Mystery database file. |
| `--model MODEL` | `OPENAI_MODEL`, or `gpt-5.6-sol` when unset | Select the Responses API model. |
| `--reasoning-effort LEVEL` | `medium` | Set reasoning effort to `none`, `low`, `medium`, `high`, `xhigh`, or `max`. Higher effort may improve the investigation but can increase latency and token usage. |
| `--max-tool-calls NUMBER` | `30` | Stop with an error if the agent exceeds this many database queries and solution submissions. |
| `-h`, `--help` | — | Display the command-line help. |

For example, use GPT-5.6 Terra with low reasoning effort:

```powershell
py sql_mystery_agent.py `
  --model gpt-5.6-terra `
  --reasoning-effort low
```

Use a different database and permit a longer investigation:

```powershell
py sql_mystery_agent.py `
  --database C:\path\to\sql-murder-mystery.db `
  --max-tool-calls 50
```

You can also choose the default model through an environment variable:

```powershell
$env:OPENAI_MODEL = "gpt-5.6-terra"
py sql_mystery_agent.py
```

To see the built-in help:

```powershell
py sql_mystery_agent.py --help
```

### Agent tests

Run the local tests with:

```powershell
py -m unittest -v
```

On macOS or Linux:

```bash
python3 -m unittest -v
```


## Authors

* [Joon Park](https://twitter.com/JoonParkMusic)
* [Cathy He](https://twitter.com/Cathy_MeiyingHe)

## Inspiration
This murder mystery was inspired by [a crime in the neighboring Terminal City](https://github.com/veltman/clmystery "command-line murder mystery").

## Copyright and License
Original code for this project is released under [the MIT License](https://github.com/NUKnightLab/sql-mysteries/blob/master/LICENSE). 

Original text and other content is released under [Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). 

SQL query custom web components used here were adapted from code created and released to the public domain by Zi Chong Kao, creator of [Select Star SQL](https://selectstarsql.com/).

[Detective image by rambleron](https://www.vecteezy.com/vector-art/174092-clue-illustration) used under Vecteezy's free license.
