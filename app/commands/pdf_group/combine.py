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
@click.option(
    '-d',
    '--output-directory',
    default="/Users/bernadette/Downloads",
    help="The destination directory for the combined and downloaded PDFs."
) 
@click.option(
    '-n',
    '--output-file-name-without-extension',
    default="output",
    help="The base file name for the combined and downloaded PDFs."
) 
@click.argument('webpage_urls', nargs=-1)
def combine_pdfs(
    count: int,
    output_directory: str,
    output_file_name_without_extension: str,
    webpage_urls: tuple[str, ...],
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
