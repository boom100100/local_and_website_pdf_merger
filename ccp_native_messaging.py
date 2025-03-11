#!/usr/bin/env python3

"""Convert and Combine PDFs Native Messaging."""

import os
import sys
import json
import struct

# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
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

def get_flag_string(flag, receivedMessage):
    VALUE = receivedMessage[flag]
    return f'{flag} {VALUE}' if receivedMessage[flag] else ''

def get_env_var_string_and_env_var_toggle_flag(
        VAR_NAME: str,
        env_vars_message,
        var_flag: str
) -> tuple[str, str]:
    if value := env_vars_message[VAR_NAME]:
        env_var_string = json.dumps(value)

        return env_var_string, var_flag

    return "", ""

# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

while True:
    receivedMessage = getMessage()
    # TODO: add security checks for these receivedMessage input values
    # and convert arrays to json
    env_vars = receivedMessage["env_vars"]

    string_flag_tuples = []
    for var_name, var_flag in (
        ("OUTPUT_DIRECTORY", "-d"),
        ("LOCAL_FILE_PATHS", "-l"),
        ("WEBPAGE_URLS", "-w"),
    ):
        string_flag_tuple = get_env_var_string_and_env_var_toggle_flag(
            var_name,
            env_vars,
            var_flag
        )
        string_flag_tuples.append(string_flag_tuple)

    OUTPUT_DIRECTORY = json.dumps(env_vars["OUTPUT_DIRECTORY"])
    OUTPUT_DIRECTORY_D = receivedMessage["-d"]
    output_directory_value = f'-d {OUTPUT_DIRECTORY_D}' if receivedMessage["-d"] else ''

    count_value = get_flag_string("-c", receivedMessage)

    OUTPUT_FILE_NAME_WITHOUT_EXTENSION = receivedMessage["-n"]
    output_file_name_without_extension_value = get_flag_string("-n", receivedMessage)

    TOGGLE_FLAGS = receivedMessage["TOGGLE_FLAGS"]
    toggle_flag_value = f'-{TOGGLE_FLAGS}' if TOGGLE_FLAGS else ''

    # macos
    if sys.platform in ("darwin", "linux"):
        os.system(f'{local_file_paths_value} {webpage_urls_value} {OUTPUT_DIRECTORY=} flask pdf combine {toggle_flag_value}')

    # windows
    if sys.platform in ("win32",):
    # if sys.platform == "win32":
    # if str(sys.platform) == "win32":
    # if sys.platform is "win32":
        ...
        # TODO: fix this line os.system(f'''set {LOCAL_FILE_PATHS=} && set {WEBPAGE_URLS=} && set {OUTPUT_DIRECTORY=} && flask pdf combine -lwxo''')
    # TODO: What to send back?
    sendMessage(encodeMessage("success 200"))
