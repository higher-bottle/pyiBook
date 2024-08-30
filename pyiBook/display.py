from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import pandas as pd


def show_tables(dataframe,title):
    table = Table(title=title, title_style="magenta", show_header=True, header_style='bold magenta', border_style='bold')
    console = Console()
    table.add_column("Index", style="bold")
    for col in dataframe.columns:
        table.add_column(col)

    for i, row in zip(dataframe.index, dataframe.values):
        table.add_row(str(i+1), *[str(item) for item in row])

    console.print(table)


def display_introduction():
    """Display an introduction using rich."""
    console = Console()
    intro_text = Text("📖 Welcome to the Export iBook Highlights CLI Tool 📖", style="bold magenta")
    description_text = Markdown(
        '''This tool helps you extract the **NOTEs, HIGHLIGHTs and their STYLEs** with your **local iBooks library** directly from the command line.  
        Please follow https://github.com/higher-bottle/pyiBook to get more **detailed Instruction, Updates, Information, and Feedback**, many thanks.  
        **Let's get started** 🎉''',
        style="cyan"
    )
    panel = Panel(
        description_text,
        title=intro_text,
        border_style="green",
    )
    console.print(panel)
