import click
from .display import display_introduction, show_tables
from .poccess import local_ibook_directory, connect_to_db


@click.group()
def cli():
    """Command-line interface for interacting with iBooks data."""
    pass


def get_db_paths():
    """Helper function to handle user input for db_path."""
    while True:
        use_default = click.prompt(click.style("Do you want to use the default path of Apple Book(Recommend)? (Y/N)", fg='green'),
                                   type=str, default="Y")
        if use_default.lower() == "n":
            db_path = click.prompt('Please input your database path', type=str)
        else:
            db_path = None

        db_paths = local_ibook_directory(db_path)

        if all(db_paths.values()):
            return db_paths.get('book_db'), db_paths.get('note_db')
        else:
            if not any([db_paths.get('book_path'), db_paths.get('note_path')]):
                click.echo(click.style("The path is not valid. Please try another one.", fg='red'))
            elif not any([db_paths.get('book_db'), db_paths.get('note_db')]):
                click.echo(click.style("There's no database file in the given path. Please try another one.", fg='red'))

            if click.confirm(click.style("Do you want to change the path? (Press N to quit)", fg='red')):
                continue
            else:
                click.echo(click.style("Exiting.", fg="green"))
                exit()


@cli.command()
@click.option('--all', 'option', flag_value='all', help='Print all records.')
@click.option('--all-book', 'option', flag_value='book', help='Print all book records.')
@click.option('--all-pdf', 'option', flag_value='pdf', help='Print all pdf records.')
@click.option('--bookname', default=None,
              help='Print records with the specified book names (comma-separated).')
@click.option('-output', 'output', is_flag=True, help='Output the result to a CSV file.')
def highlights(option, bookname, output):
    """Print or output iBook highlights based on the specified criteria."""
    display_introduction()
    book_db_path, notation_db_path = get_db_paths()
    df_book, df_notation = connect_to_db(book_db_path, notation_db_path)
    df_result = None

    if option == 'all':
        df_result = df_book
    elif option == 'book':
        df_result = df_book[df_book['FileType'] == 'Book']
    elif option == 'pdf':
        df_result = df_book[df_book['FileType'] == 'pdf']
    elif bookname:
        booknames = [name.strip() for name in bookname.split(',')]
        df_result = df_book[df_book['BookName'].str.contains('|'.join(booknames), case=False, na=False)]

        missing_books = [name for name in booknames if
                         not df_result['BookName'].str.contains(name, case=False, na=False).any()]
        if missing_books:
            click.echo(click.style(f"Cannot find the following books: {', '.join(missing_books)}", fg='red'))
            output = False

    # click.echo(click.style("Selected Books Info:",fg='green', bold=True))
    show_tables(df_result[df_result.columns.difference(['ID'])], 'Books Info')

    if output:
        # click.echo(click.style("Here is the preview(10 lines) of the output file.", fg='green', bold=True))
        df_result_notation = df_notation[df_notation['ID'].isin(df_result['ID'])]
        show_tables(df_result_notation[df_result_notation.columns.difference(['ID'])].head(10),
                    'Preview(10 lines) of the Output file')

        file_name = click.prompt(click.style('Please give the file name',fg='green',bold=True), type=str)
        file_type_choose = click.prompt(click.style("CSV or XLSX file? Recommend XLSX for Chinese notes.(a:csv/b:xlsx)",
                                                    fg='green', bold=True),
                                        type=click.Choice(['a', 'b']), default="a")

        file_type = 'csv' if file_type_choose == 'a' else 'xlsx'
        # output_filename = os.path.join(os.getcwd(),'Output', f"{file_name}.{file_type}")
        output_filename = f"{file_name}.{file_type}"

        if file_type_choose == 'a':
            df_result_notation.to_csv(output_filename, index=False)
        else:
            df_result_notation.to_excel(output_filename, index=False)

        click.echo(click.style(f"Output saved to {output_filename}", fg='green', bold=True))
