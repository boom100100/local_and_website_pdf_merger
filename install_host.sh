#!/bin/sh
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file at https://github.com/GoogleChrome/chrome-extensions-samples/blob/main/LICENSE.

set -e

DIR="$1"
if [ $(uname -s) == 'Darwin' ]; then
    TARGET_DIR="/Library/Google/Chrome/NativeMessagingHosts"
  # if [ "$(whoami)" == "root" ]; then
    # TARGET_DIR="/Library/Google/Chrome/NativeMessagingHosts"
  #   # chmod a+x "$DIR/native-messaging-example-host"
  # else
  #   TARGET_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
  # fi
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
sudo mv "$DIR/$HOST_NAME.json.macos" "$TARGET_DIR/$HOST_NAME.json"

# Update host path in the manifest.
HOST_PATH="$DIR"
ESCAPED_HOST_PATH=${HOST_PATH////\\/}
sudo sed -i -e "s/HOST_PATH/$ESCAPED_HOST_PATH/" "$TARGET_DIR/$HOST_NAME.json"
sudo rm "$TARGET_DIR/com.automatedbooks.convert_and_combine_pdfs.json-e" # todo: fix this file name error

# Set permissions for the manifest so that all users can read it.
chmod o+r "$TARGET_DIR/$HOST_NAME.json"

# trigger chrome extension installation
chmod 755 ./install_chrome_extension.sh
./install_chrome_extension.sh diefpbmcaopdlphclenlgfcmeafacojg

# make native messaging app executable
chmod 755 native_host.py

echo Native messaging host $HOST_NAME has been installed.
