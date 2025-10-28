import os
import json
from typing import Optional
from rich.text import Text
from rich.console import Console
from rich.table import Table, Column
from rich import box
from typing_extensions import Annotated

import typer
from .utils import Utils
from .config import Config
from .db.db_client import DBClient
from .models.expense import Expense
from .models.output_format import FileFormat

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
def summary(
    month: Annotated[str, typer.Option(help="Month of the year. eg: Jan, Feb.")],
    year: Annotated[str, typer.Option(
        help="The year in the format YYYY. eg: 2025")]
):
    """
    Display a summary of the expenses based on the month and year
    """
    try:
        monthOrdinal = Utils.month_text_to_ordinal(month)
        summary = DBClient.summary(monthOrdinal, year)
        if len(summary) == 0:
            console.print("No transactions this month.")
            return
        total_spent = sum([row.amount for row in summary])
        table_min_width = 70
        table = Table(
            Column(header="Category", justify="left"),
            Column(header="Total", justify="left"),
            Column(footer="Total"),
            Column(footer=f"{Utils.format_currency(total_spent)}"),
            title=f"{Utils.month_short_to_full(month)} Summary",
            title_style="bold",
            title_justify="left",
            show_lines=True,
            min_width=table_min_width,
            box=box.SIMPLE,
            show_footer=True,
        )
        for row in summary:
            bar = "█" * int((row.amount / total_spent) * table_min_width)
            table.add_row(
                row.category, f"{bar} {Utils.format_currency(row.amount)}")
        console.print()
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def export(
    output: Annotated[typer.FileTextWrite, typer.Option()],
    _format: Annotated[
        FileFormat,
        typer.Option("--format", case_sensitive=False)
    ] = FileFormat.CSV
):
    """Export recorded expenses to a file"""
    try:
        expenses = DBClient.get_all()
        match _format:
            case FileFormat.CSV:
                expenses_csv_format = [
                    f"{expense.to_csv()}\n"
                    for expense in expenses
                ]
                output.write("ID,Amount,Description,Category,Date\n")
                output.writelines(expenses_csv_format)
            case FileFormat.JSON:
                expenses_dict_format = [expense.to_dict()
                                        for expense in expenses]
                expenses_json = json.dumps(expenses_dict_format)
                output.write(expenses_json)
        console.print(
            f"Exported expenses to: [bold yellow]{output.name}[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="import")
def import_expenses(
    file: Annotated[str, typer.Option(help="File containing expenses")],
    _format: Annotated[
        FileFormat,
        typer.Option("--format", case_sensitive=False)
    ] = FileFormat.CSV
):
    """Import expenses from a file. Supports CSV and JSON"""
    expenses = []
    try:
        match _format:
            case FileFormat.CSV:
                expenses = Expense.parse_csv(file)
            case FileFormat.JSON:
                expenses = Expense.parse_json(file)
        imported_count = len(expenses)
        DBClient.add_many(expenses)
        console.print(
            f"Imported {imported_count} expenses from: [bold yellow]{file}[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
