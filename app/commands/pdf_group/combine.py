import click

from app.commands.groups import pdf_cli
from app.services import Document, Pdf


@pdf_cli.command('combine') 
@click.option(
    '-c',
    '--count',
    default=1,
    help='Number of existing files.'
)
@click.argument('output_directory', default="~/Downloads") 
@click.argument('output_file_name_without_extension', default="output")
@click.argument('webpage_urls', nargs=-1)
# default="",
# required=False,
def combine_pdfs(
    count: int, # TODO: validate that the supplied arg for this parameter can convert to an int
    output_directory: str,
    output_file_name_without_extension: str,
    webpage_urls: tuple[str, ...], # TODO: should this support more than one at a time?
):
    existing_file_paths = Document.select(
        int(count)
    )

    Pdf.combine(
        existing_file_paths,
        webpage_urls,
        output_file_name_without_extension,
        output_directory
    )
