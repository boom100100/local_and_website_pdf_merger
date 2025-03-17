#!/bin/sh
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -e

DIR="$( cd "$( dirname "$0" )" && pwd )"
if [ $(uname -s) == 'Darwin' ]; then
  if [ "$(whoami)" == "root" ]; then
    TARGET_DIR="/Library/Google/Chrome/NativeMessagingHosts"
    # chmod a+x "$DIR/native-messaging-example-host"
  else
    TARGET_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
  fi
else
  if [ "$(whoami)" == "root" ]; then
    TARGET_DIR="/etc/opt/chrome/native-messaging-hosts"
    # chmod a+x "$DIR/native-messaging-example-host"
  else
    TARGET_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
  fi
fi

HOST_NAME=com.automatedbooks.convert_and_combine_pdfs

# Create directory to store native messaging host.
mkdir -p "$TARGET_DIR"

# Substitute directory specified in the path value with an absolute path
echo -e $(sed -e "s|pwd|$PWD|" "com.automatedbooks.convert_and_combine_pdfs.json.macos") > "com.automatedbooks.convert_and_combine_pdfs.json.macos"

# Move macos manifest to .json
mv "$DIR/$HOST_NAME.json.macos" "$TARGET_DIR/$HOST_NAME.json"

# Copy native messaging host manifest.
cp "$DIR/$HOST_NAME.json" "$TARGET_DIR"

# Update host path in the manifest.
HOST_PATH="$DIR"
ESCAPED_HOST_PATH=${HOST_PATH////\\/}
sed -i -e "s/HOST_PATH/$ESCAPED_HOST_PATH/" "$TARGET_DIR/$HOST_NAME.json"

# Set permissions for the manifest so that all users can read it.
chmod o+r "$TARGET_DIR/$HOST_NAME.json"

# trigger chrome extension installation
mkdir "$HOME/Library/Application Support/Google/Chrome/External Extensions"
echo -e '{\n"external_update_url": "https://chrome.google.com/webstore/download/diefpbmcaopdlphclenlgfcmeafacojg/revision/00001/package/main/crx/3"\n}' >> "$HOME/Library/Application Support/Google/Chrome/External Extensions/diefpbmcaopdlphclenlgfcmeafacojg.json"

# make native messaging app executable
chmod 755 native_host.py

echo Native messaging host $HOST_NAME has been installed.
