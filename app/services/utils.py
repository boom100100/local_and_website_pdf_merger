import os


def get_unique_file_name(
    output_directory: str,
    output_file_name_without_extension: str
) -> str:
    output_path = f"{output_directory}/{output_file_name_without_extension}.pdf"
    counter = 1

    while os.path.isfile(output_path):
        output_path = f"{output_directory}/{output_file_name_without_extension} ({counter}).pdf"
        counter += 1
    
    return output_path
