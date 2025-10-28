# CLI Expense Tracker

A terminal based CLI expense tracker built with _[Python](https://www.python.org/)_ and _[Typer](https://typer.tiangolo.com/)_.
You can log all your expenses and auto-categorise them with a few commands in the terminal.
The CLI also provides a concise summary of expenses which can be filtered by month and year.

---

## Features

- **Add** expenses
- **Auto Categorise** expenses based on keywords in the description
- **Spending Summaries** filtered by month and year
- **Export / Import** expenses in JSON or CSV

---

## Examples

```bash
$ python -m expense_tracker.main add 55.4 "Quick meal at McDonald's"
Added: $55.40 for Quick meal at McDonald's

# '--name' is used when the DB_NAME environment variable is not set
$ python -m expense_tracker.main --name expenses add 101.4 "LogiTech MX Keyboard"
Added: $101.40 for LogiTech MX Keyboard

$ python -m expense_tracker.main summary --month Oct --year 2025
October Summary

  Category        Total
 ───────────────────────────────────────────────────────────────────────
  Food & Drinks   ████████████████████ $75.90

  None            ███████████████████████████ $101.66

  Other           ██████████████████████ $83.00
 ───────────────────────────────────────────────────────────────────────
                                                        Total   $260.56
```

---

## Installation

### Requirements

- Python 3.9+
- Pip

### Setup

```bash
# Clone repository
git clone https://github.com/gerald-tetteh/expense-tracker-cli.git
cd expense_tracker-cli

# Setup virtual environment (optional)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Before running you can setup the 'DB_NAME' or using the '--name' option before the command
export DB_NAME=expenses
python -m expense_tracker.main --name <db-name> <command>
```

---

## Tech Stack

- [Typer](https://typer.tiangolo.com/)
- SQLite
- [Python](https://www.python.org/)

## Planned Features

- Allow categories to be configured through a config file.
