#!/usr/bin/env python3

"""Convert and Combine PDFs Native Messaging."""

from enum import Enum
import shlex
import subprocess
import sys
import json
import struct

# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    print(sys.stdin)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    return json.loads(message)

# Encode a message for transmission, given its content.
def encodeMessage(messageContent):
    # https://docs.python.org/3/library/json.html#basic-usage
    # To get the most compact JSON representation, you should specify
    # (',', ':') to eliminate whitespace.
    # We want the most compact representation because the browser rejects
    # messages that exceed 1 MB.
    encodedContent = json.dumps(messageContent, separators=(',', ':')).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}

class SystemName(str, Enum):
    WINDOWS = 'win32'
    MACOS = "macos"

def get_command(system: str, options: dict) -> str:
    cli_command = "flask pdf combine"

    env_var_name_value_flag_tuples: list[tuple[str, str, str]] = options.get("env_var_name_value_flag_tuples")
    count_value = options.get("count_value")
    output_file_name_without_extension_value = options.get("output_file_name_without_extension_value")
    should_open_output_file = options.get("should_open_output_file", "")
    should_delete_downloaded_files = options.get("should_delete_downloaded_files", "")

    if system == SystemName.WINDOWS:
        # set env vars
        for env_var_name, env_var_value, env_var_flag in env_var_name_value_flag_tuples:
            cli_command = f'set {env_var_name}={env_var_value} && {cli_command} {env_var_flag}'

        # set optional flags and their values
        # TODO: the value here may need quotes around it
        for value in [
            count_value,
            output_file_name_without_extension_value,
            should_open_output_file,
            should_delete_downloaded_files,
        ]:
            cli_command = f'{cli_command} {value}'
        # return f'''set {LOCAL_FILE_PATHS=} && set {WEBPAGE_URLS=} && set {OUTPUT_DIRECTORY=} && flask pdf combine -lwxo'''
        return cli_command

    if system == SystemName.MACOS:
        # set env vars
        for env_var_name, env_var_value, env_var_flag in env_var_name_value_flag_tuples:
            if not env_var_name:
                continue
            # TODO: should this be a conditional json.dumps instead? An array requires it, but it'll probably break for a string.
            # TODO: should sanitize these inputs
            
            # TODO: this is a workaround. test for if nesting may break this.
            env_var_value = r"".join('"' if c == "'" else c for c in str(env_var_value)) # convert ' to "
            env_var_value = "".join(f'\{c}' if c in ('"', "'") else c for c in env_var_value) # escape " and '

            # # if isinstance(env_var_value, list):
            # #     env_var_value = json.dumps(env_var_value)
            # # cli_command = rf"{env_var_name}='{env_var_value}' {cli_command} {env_var_flag}"
            # # # cli_command = f"{env_var_name}='{env_var_value}' {cli_command} {env_var_flag}"
            # # # cli_command = f'{env_var_name}=\'{env_var_value}\' {cli_command} {env_var_flag}'
            # # # cli_command = f"{env_var_name}=\'{env_var_value}\' {cli_command} {env_var_flag}"
            cli_command = rf"{env_var_name}=\'{env_var_value}\' {cli_command} {env_var_flag}"
            # cli_command = rf"{env_var_name}='{env_var_value}' {cli_command} {env_var_flag}"
            # cli_command = f"{env_var_name}={"'"}{env_var_value}{"'"} {cli_command} {env_var_flag}"
            # # cli_command = f'{env_var_name}={"'"}{env_var_value}{"'"} {cli_command} {env_var_flag}'
            # # f"{"'"}{json.dumps(["https://www.reddit.com/r/learnjavascript/comments/mz7a\
            # # o/access_global_variables_in_content_scriptchrome/"])}{"'"}"

        # set optional flags and their values
        for value in [
            count_value,
            output_file_name_without_extension_value,
            should_open_output_file,
            should_delete_downloaded_files,
        ]:
            cli_command = f'{cli_command} {value}'

        # json_workaround = ""
        # for c in cli_command:
        #     if c == '"':
        #         json_workaround += "'"
        #     elif c == "'":
        #         json_workaround += '"'
        #     else:
        #         json_workaround += c
        # cli_command = json_workaround
        # f'{''}'
        return cli_command

    return ""

def get_option_flag_string(flag: str, receivedMessage: dict, should_wrap: bool, should_sanitize: bool) -> str:
    VALUE = receivedMessage.get(flag)
    if VALUE:
        sanitized_value = sanitize_value(VALUE) if should_sanitize else VALUE
        sanitized_wrapped_value = f'"{sanitized_value}"' if should_wrap else sanitized_value
        return f'{flag} {sanitized_wrapped_value}'
    return ""
        

def get_env_var_name_value_flag_tuple(
        env_var_name: str,
        env_vars_message: dict,
        env_var_flag: str
) -> tuple[str, str, str]:
    if env_var_value := env_vars_message.get(env_var_name):
        return env_var_name, env_var_value, env_var_flag if env_var_flag != "-d" else ""

    return "", "", ""

def sanitize_value(value: str) -> str:
    return "".join(
        character
        if character.isalnum() or character == " " 
        else "_" 
        for character in value
    )

# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

while True:
    receivedMessage: dict = getMessage()
    print(receivedMessage)

    # TODO: add security checks for these receivedMessage input values
    env_vars: dict = receivedMessage.get("env_vars", {})

    # if "LOCAL_FILE_PATHS" in env_vars.keys():
    #     for i in range(0, len(env_vars["LOCAL_FILE_PATHS"])):
    #         env_vars["LOCAL_FILE_PATHS"][i] = sanitize_value(env_vars["OUTPUT_DIRECTORY"])



    env_var_name_value_flag_tuples: list[tuple[str, str, str]] = []
    WEBPAGE_URLS_str: str
    for var_name, var_flag in (
        ("WEBPAGE_URLS", "-w"),
    ):
        name, value, flag = get_env_var_name_value_flag_tuple(
            var_name,
            env_vars,
            var_flag
        )
        WEBPAGE_URLS_str = value
    for var_name, var_flag in (
        ("OUTPUT_DIRECTORY", "-d"),
        ("LOCAL_FILE_PATHS", "-l"),
        ("WEBPAGE_URLS", "-w"),
    ):
        env_var_name_value_flag_tuple = get_env_var_name_value_flag_tuple(
            var_name,
            env_vars,
            var_flag
        )
        env_var_name_value_flag_tuples.append(env_var_name_value_flag_tuple)

    count_value = get_option_flag_string("-c", receivedMessage, False, False)
    output_file_name_without_extension_value = get_option_flag_string("-n", receivedMessage, True, True)
    should_open_output_file = "-o" if receivedMessage.get("-o") else ""
    should_delete_downloaded_files = "-x" if receivedMessage.get("-x") else ""

    # macos
    if sys.platform in ("darwin", "linux"):
        system_name = "macos"
        options = {
            "env_var_name_value_flag_tuples": env_var_name_value_flag_tuples,
            "count_value": count_value,
            "output_file_name_without_extension_value": output_file_name_without_extension_value,
            "should_open_output_file": should_open_output_file,
            "should_delete_downloaded_files": should_delete_downloaded_files,
        }
        get_command(system_name, options)

    # windows
    elif sys.platform in ("win32",):
    # elif sys.platform == "win32": # this causes code to be unreachable for some reason
        system_name = "windows"
        
    else:
        sendMessage(encodeMessage("failed os match not found"))
        break

    cli_command = get_command(system_name, options)
    if not cli_command:
        sendMessage(encodeMessage("failed launch command not constructed"))
        break

#     # # # res = os.system("not_a_command_xxxxxxxxxxxxxxxx")
#     # # # res = os.system("flask pdf combine")
#     # # # res = os.system(f'pipenv shell "flask pdf combine"')
#     # # # res = None
#     # # # res = os.system("pwd")
#     # # import os
#     # # # res = os.system(cli_command)
#     # # res = os.system(f'pipenv shell "{cli_command}"')
#     # result = subprocess.check_output(executable=cli_command)
#     # result = subprocess.Popen(executable=cli_command)
#     # subprocess.Popen(cli_command)
    command = shlex.split(cli_command)
    # process = subprocess.run(command)
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     # process = subprocess.Popen(command)
#     # subprocess.Popen(cli_command, shell=True)
#     # result = subprocess.check_output(executable=f'pipenv shell "{cli_command}"')
#     # # result = subprocess.check_output(["pipenv", "shell", f'"{cli_command}"'])
#     # # """
#     # # WEBPAGE_URLS='["https://www.reddit.com/r/learnjavascript/comments/mz87ao/access_global_variables_in_content_scriptchrome/"]' OUTPUT_DIRECTORY='./outputs' flask pdf combine  -w -c 1 -n "Access global variables in content script_chrome extension_ _ r_learnjavascript resume" -o -x
#     # # import os
#     # # os.system(cli_command)
# #     """
# # WEBPAGE_URLS='["https://stackoverflow.com/questions/74836530/in-a-chrome-extension-cant-send-a-message-from-the-content-script-to-the-backg"]' OUTPUT_DIRECTORY='./outputs' flask pdf combine  -w -c 1 -n "javascript _ In a chrome extension_ can_t send a message from the content script to the background script and get a response _ Stack Overflow resume" -o -x"
# #     """

#     # # """



    # TODO: What to send back?
    sendMessage(encodeMessage({
        "cli_cmd": cli_command,
        "cmd": command, 
        "code": 200,
        # "stdout": stdout,
        # "stderr": stderr,
    }))
    # sendMessage(encodeMessage(f"{WEBPAGE_URLS_str}\n\n{cli_command}"))
    # sendMessage(encodeMessage("success 200 resume path? output path?"))
