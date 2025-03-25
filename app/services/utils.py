import os
import pathlib
import platform
import subprocess


def delete_files(file_paths, condition):
    if condition:
        for path in file_paths:
            if os.path.isfile(path):
                file_to_rm = pathlib.Path(path)
                file_to_rm.unlink(missing_ok=True)

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


def open_file(path: str, condition: bool) -> None:
    # including isfile check to make sure there's no weird injection activity. 
    # TODO: validate need for this further.
    if condition and os.path.isfile(path):
        if system := platform.system() == "Windows":
            command = os.startfile
        elif system == "Darwin":
            command = lambda path: subprocess.Popen(("open", path), stdout=subprocess.PIPE).communicate()
        else:
            command = lambda path: None

        command(path)
