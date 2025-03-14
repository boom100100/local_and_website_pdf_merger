import click
import sys
import json

from app.commands.pdf_group import combine_pdfs


def main():
    data=json.loads(sys.argv[1])
    click_context = click.Context(combine_pdfs)

    # TODO: don't hardcode these
    count = 1
    output_directory = "./outputs"
    # output_directory = "/Users/bernadette/Applications/convert_and_combine_pdfs/outputs"
    should_use_local_file_paths = False
    should_use_webpage_urls  = False
    output_file_name_without_extension = "test output resume"
    should_open_output_file = True
    delete_downloaded_files = True
    webpage_urls = (
        "https://www.google.com",
    )

    click_context.invoke(
        combine_pdfs,
        count=count,
        output_directory=output_directory,
        should_use_local_file_paths=should_use_local_file_paths,
        should_use_webpage_urls=should_use_webpage_urls,
        output_file_name_without_extension=output_file_name_without_extension,
        should_open_output_file=should_open_output_file,
        delete_downloaded_files=delete_downloaded_files,
        webpage_urls=webpage_urls,
    )


if __name__ == '__main__':
    main()
