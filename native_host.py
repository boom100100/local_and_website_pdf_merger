#!/usr/bin/env python3

"""Convert and Combine PDFs Native Messaging."""

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

# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

while True:
    receivedMessage: dict = getMessage()
    process = subprocess.Popen(
        [
            ".venv/bin/python3",
            "./invoke_combine_pdfs.py", # also works
            # TODO: it's obviously not necessary to constantly pass these values to json.dumps and json.loads, but I'm going to leave it in as a reminder of the nature of network data. I think that's fine, since this initial app isn't meant to send massive amounts of webpage url data and since it won't run on a remote/paid server.
            json.dumps(receivedMessage),
        ],
        stdout=subprocess.PIPE
    )
    stdout, stderr = process.communicate(timeout=20)


    # TODO: What to send back?
        # saved file name.
        # everything else in request should be browser settings (from the chrome extension)
    sendMessage(encodeMessage({
        "code": 200,
        "res": None,
        # "executable_paths": os.environ.get("PATH")
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
    }))
