import os
import platform

platform_command_map = {
    "Darwin": {
        "launch": "open",
        "delete": "rm",
    },
    "Windows": {
        "launch": "explorer",
        "delete": "del",
    },
}
def get_platform_specific_cmd(command_name: str) -> str:
    return platform_command_map[platform.system()][command_name]

def delete_files(file_paths, condition):
    if condition:
        for path in file_paths:
            if os.path.isfile(path):
                os.system(f'{get_platform_specific_cmd("delete")} "{path}"')

        files_string = '\n'.join(file_paths)
        print("Finished deleting files:\n\n")
        print(files_string)


def get_unique_file_name(
    output_directory: str,
    output_file_name_without_extension: str
) -> str:
    previous_name = f"{output_file_name_without_extension}.pdf"
    final_name = previous_name
    counter = 1

    while os.path.isfile(f"{output_directory}/{final_name}"):
        final_name = f"{output_file_name_without_extension} ({counter}).pdf"
        counter += 1
    
    return final_name

def open_file(path: str, condition: bool):
    # including isfile check to make sure there's no weird injection activity. 
    # TODO: validate need for this further.
    if condition and os.path.isfile(path):
        os.system(f'{get_platform_specific_cmd("launch")} "{path}"')
