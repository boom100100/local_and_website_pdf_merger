import click
import json
import os

from app.commands.groups import pdf_cli
from app.services import Document, Pdf


@pdf_cli.command('combine', context_settings={'show_default': True}) 
@click.option(
    '-c',
    '--count',
    default=1,
    help='Number of local files to merge. Choose 0 to skip selecting local files.'
)
@click.option(
    '-d',
    '--output-directory',
    default="/Users/bernadette/Downloads",
    help="The destination directory for the combined and downloaded PDFs."
) 
@click.option(
    '-l',
    '--use-local-file-paths',
    is_flag=True,
    help="""Identify local PDF(s) via LOCAL_FILE_PATHS in `.env` as a json array instead of choosing them via the GUI.
This will ignore the count (-c, --count) flag.
Example: $ LOCAL_FILE_PATHS='["/Users/bernadette/Downloads/Bernadette Davis Professional Resume Long.pdf"]' flask pdf combine -l <optional-webpage>
"""
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
    use_local_file_paths: bool,
    output_file_name_without_extension: str,
    webpage_urls: tuple[str, ...],
) -> None:
    if use_local_file_paths:
        existing_file_paths = json.loads(os.environ['LOCAL_FILE_PATHS'])
    else:
        existing_file_paths = Document.select(
            int(count)
        )

    Pdf.combine(
        existing_file_paths,
        webpage_urls,
        output_file_name_without_extension,
        output_directory
    )
