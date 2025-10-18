import locale

import typer
from.utils import Utils
from typing_extensions import Annotated
from rich.console import Console
from rich.text import Text

app = typer.Typer()
console = Console()

@app.command()
def add(amount: Annotated[float, typer.Argument()], description: Annotated[str, typer.Argument()]):
    """
    Add a new expense.
    """
    # logic to add expense
    text = Text()
    text.append("Added: ")
    text.append(f"{Utils.format_currency(amount)}", style="bold green")
    text.append(f" for ")
    text.append(f"{description}", style="italic yellow")
    console.print(text)

@app.command()
def list():
    """
    List all expenses.
    """
    # logic to list expenses
    console.print("Listing all expenses...")