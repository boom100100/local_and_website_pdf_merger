from typing import Optional
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
    default=None,
    help="""The destination directory for the combined and downloaded PDFs.
Set the environmental variable OUTPUT_DIRECTORY or supply an argument via the flag. The flag value overrides the environment variable."""
) 
@click.option(
    '-l',
    '--should-use-local-file-paths',
    is_flag=True,
    help="""Identify local PDF(s) via the LOCAL_FILE_PATHS environmental variable as a json array instead of choosing them via the GUI.
This will ignore the count (-c, --count) flag.
Example: $ LOCAL_FILE_PATHS='["/Users/bernadette/Downloads/Bernadette Davis Professional Resume Long.pdf"]' flask pdf combine -l <optional-webpage>
"""
) 
@click.option(
    '-w',
    '--should-use-webpage-urls',
    is_flag=True,
    help="""Identify webpage(s) to convert to PDF via the WEBPAGE_URLS environmental variable as a json array instead of choosing them via argument inputs.
Activating this flag causes overwriting all of the `webpage_urls` arguments.
Example: $ WEBPAGE_URLS='["https://www.google.com"]' flask pdf combine -w
"""
) 
@click.option(
    '-n',
    '--output-file-name-without-extension',
    default="output",
    help="The base file name for the combined and downloaded PDFs."
) 
@click.option(
    '-o',
    '--should-open-output-file',
    is_flag=True,
    help="Open the combined file or the single file when the process is complete."
)
@click.option(
    '-x',
    '--delete-downloaded-files',
    is_flag=True,
    help="Delete downloaded PDFs. If also activated, the open (-o, --should-open-output-file) flag overrides this when 1 webpage and 0 local PDFs are selected to be combined."
)
# @click.option(
#     '-sf',
#     is_flag=True,
#     help="Save local file paths." # TODO: is this neecssary?
# )
@click.argument('webpage_urls', nargs=-1)
def combine_pdfs(
    count: int,
    output_directory: Optional[str],
    should_use_local_file_paths: bool,
    should_use_webpage_urls: bool,
    output_file_name_without_extension: str,
    should_open_output_file: bool,
    delete_downloaded_files: bool,
    webpage_urls: list[str],
    # sf: bool,
) -> None:
    # TODO: enable reordering. All existing will always be before all webpage downloads.
    if should_use_local_file_paths:
        existing_file_paths = json.loads(os.environ['LOCAL_FILE_PATHS'])
    else:
        existing_file_paths = Document.select(
            int(count)
        )

    if should_use_webpage_urls:
        webpage_urls = json.loads(os.environ['WEBPAGE_URLS'])

    if not output_directory:
        os.environ.get("OUTPUT_DIRECTORY", "./outputs")

    Pdf(
        existing_file_paths,
        webpage_urls,
        output_file_name_without_extension,
        output_directory,
        should_open_output_file,
        delete_downloaded_files,
    ).combine()
