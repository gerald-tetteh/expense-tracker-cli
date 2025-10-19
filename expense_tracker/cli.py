from rich.text import Text
from rich.console import Console
from typing_extensions import Annotated
import locale

import typer
from .utils import Utils

app = typer.Typer()
console = Console()


@app.command()
def init(name: Annotated[str, typer.Argument(help="Refers to the users' whose expenses are being tracked.")]
         ):
    pass


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
