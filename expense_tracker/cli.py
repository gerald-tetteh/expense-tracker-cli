import os
from typing import Optional
from rich.text import Text
from rich.console import Console
from typing_extensions import Annotated

import typer
from .utils import Utils
from .config import Config
from .db.db_client import DBClient
from .models.expense import Expense

app = typer.Typer()
console = Console()


@app.callback()
def main(name: Annotated[Optional[str], typer.Option(
        help=f"Refers to the users' whose expenses are being tracked. Can be set through and environment variable {Config.ENV_DB_NAME}")] = None):
    """
    Expense Tracker CLI Application.
    """
    if (name is not None):
        os.environ[Config.ENV_DB_NAME] = name


@app.command()
def init(
        name: Annotated[Optional[str], typer.Option(
            help=f"Refers to the users' whose expenses are being tracked. Can be set through and environment variable {Config.ENV_DB_NAME}")] = None):
    """
    Initialize the expense tracker for a user.
    """
    if (name is not None):
        os.environ[Config.ENV_DB_NAME] = name
    try:
        DBClient.init_db()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
    console.print(
        f"Expense tracker initialized for [bold blue]{os.environ[Config.ENV_DB_NAME]}[/bold blue].")


@app.command()
def add(amount: Annotated[float, typer.Argument()], description: Annotated[str, typer.Argument()]):
    """
    Add a new expense.
    """
    # logic to add expense
    try:
        expense = Expense(amount, description)
        DBClient.add(expense.to_dict())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
    text = Text()
    text.append("Added: ")
    text.append(f"{Utils.format_currency(amount)}", style="bold green")
    text.append(f" for ")
    text.append(f"{description}", style="italic yellow")
    console.print(text)


@app.command()
def list(
    month: Annotated[str, typer.Option(help="Month of the year. eg: Jan, Feb.")],
    year: Annotated[str, typer.Option(help="The year in the format YYYY. eg: 2025")],
    page: Annotated[int, typer.Option(
        help="The page number for paginated results. Defaults to 1")] = 1,
    limit: Annotated[int, typer.Option(
        help="The number of results to return. Defaults to 20")] = 20
):
    """
    List all expenses.
    """
    try:
        monthOrdinal = Utils.month_text_to_ordinal(month)
        expenses = DBClient.list_expenses(monthOrdinal, year, page, limit)
        output = "\n".join([str(expense) for expense in expenses])

        console.print(
            f"Expenses for [bold yellow]{month}, {year}[/bold yellow]")
        typer.echo(output)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def summary():
    pass
