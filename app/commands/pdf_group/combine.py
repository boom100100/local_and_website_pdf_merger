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
Example: $ WEBPAGE_URLS='["https://www.indeed.com/viewjob?jk=95dcd405c2a1b78b&advn=5989917549446440&adid=441805480&ad=-6NYlbfkN0DnT8lSZ_ijuq54neM5qYH41HzsT327pZyT1Sudseg0NuYNTVimnpM6NxaEH2JYkHpinytEVMYIU7ZtbcfbQw5kEccXPxX56x4-3yvswwWlJ_psocHOIWDenGmb4Cw4ZErxquiDK3z3mzsIN9PAJ98nlymUWUK-6-7VMmqsdF54U7Glzptdr7TG3iEM9f7Y4CeLVRkllbUsHj1Qj4EatRaC-qxK_-0ROctOZ1GXXDb0FofmYy3LCcqlyjLjZUyOr-S86tPOCPUf4OiYC_AWLZ8UDaNtvf5mYrwOoqiyqIJGUCn80-ycdkJIIKo9im2Iyinv0YpNUZl9F5RdPrW8aSQ_GP945OeD94SAv-_1wc7g78BSbUdP5W1jeQzyigCQiAtEAufVkRNHcV8MWflRj1B14fDHkLjGAiaBgy6y3fk05ss2hQORUWkQ9HhjEGMgQrrtakLeyWZZAQ%3D%3D&from=mobRdr&dest=https%3A%2F%2Fapply.workable.com%2Fj%2FEFCB3337E9&desth=ee3b06104341ecfd9e15354814cd2979&tk=1im07p7ubl02c802&dupclk=1&acatk=1im08pg0ll53p801&pub=f3745ccc8109d6c722d9de41ee0f65f30cace3277f6b99df&camk=ethIe0s0hed-C1xiRCIL1g%3D%3D&xkcb=SoCi6_M30AHq3UiVuv0KbzkdCdPP&xpse=SoA-6_I30AZp2_3fhh0IbzkdCdPP&xfps=ed9761ca-704b-48b1-a693-2b3f517fa98e&utm_source=%2Fm%2F&utm_medium=redir&utm_campaign=dt"]' flask pdf combine -w
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
@click.argument('webpage_urls', nargs=-1)
def combine_pdfs(
    count: int,
    output_directory: str,
    should_use_local_file_paths: bool,
    should_use_webpage_urls: bool,
    output_file_name_without_extension: str,
    should_open_output_file: bool,
    webpage_urls: tuple[str, ...],
) -> None:
    if should_use_local_file_paths:
        existing_file_paths = json.loads(os.environ['LOCAL_FILE_PATHS'])
    else:
        existing_file_paths = Document.select(
            int(count)
        )

    if should_use_webpage_urls:
        webpage_urls = json.loads(os.environ['WEBPAGE_URLS'])

    Pdf.combine(
        existing_file_paths,
        webpage_urls,
        output_file_name_without_extension,
        output_directory,
        should_open_output_file,
    )
