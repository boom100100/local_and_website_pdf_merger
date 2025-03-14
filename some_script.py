import click
import os
import sys
import json

from app.commands.pdf_group import combine_pdfs


def sanitize_value(value: str) -> str:
    return "".join(
        character
        if character.isalnum() or character == " " 
        else "_" 
        for character in value
    )


def main():
    data: dict = json.loads(sys.argv[1])

    env_vars: dict = data.get("env_vars", {})

    count = data.get("-c", 0)
    output_directory = env_vars.get("OUTPUT_DIRECTORY", "./outputs") # can ignore -d flag, only one input is necessary
    # "/Users/bernadette/Applications/convert_and_combine_pdfs/outputs"


    def set_os_env_var_and_should_use(key: str, default: list) -> bool:
        # should be false for the chrome extension
        should_use = False
        if list_value := env_vars.get(key, default):
            os.environ[key] = json.dumps(list_value)
            should_use = True 

        return should_use

    # if this script is running, it can still control env vars
    should_use_local_file_paths = set_os_env_var_and_should_use("LOCAL_FILE_PATHS", [])
    should_use_webpage_urls = set_os_env_var_and_should_use("WEBPAGE_URLS", []) # can ignore webpage_urls args

    output_file_name_without_extension = sanitize_value(
        data.get("-n", "default resume")
    )
    should_open_output_file = data.get("-o", True)
    delete_downloaded_files = data.get("-x", True)
    webpage_urls = tuple()

    click_context = click.Context(combine_pdfs)
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
