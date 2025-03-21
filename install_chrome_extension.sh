#!/bin/bash

# https://developer.chrome.com/docs/extensions/mv3/external_extensions/#preferences
# source: https://gist.github.com/cezaraugusto/0101d2cb251c088f398ca0f8d4495ca0

install_chrome_extension() {
  chrome_extensions_folder="$HOME/Library/Application Support/Google/Chrome/External Extensions"
  chrome_extensions_preferences_file="$chrome_extensions_folder/$1.json"
  # This URL is used by Chrome to check for updates to external extensions
  update_services_url="https://clients2.google.com/service/update2/crx"

  mkdir -p "$chrome_extensions_folder"

  echo "{" > "$chrome_extensions_preferences_file"
  echo "  \"external_update_url\": \"$update_services_url\"" >> "$chrome_extensions_preferences_file"
  echo "}" >> "$chrome_extensions_preferences_file"

  echo "Added \"$chrome_extensions_preferences_file\""
}

if [ $# -ne 1 ]; then
  echo "Usage: $0 <extension_id>"
  exit 1
fi

install_chrome_extension "$1"

# Usage: 
# ./install_extension.sh <extension_id>
# Sample: adding React Dev Tools from command-line to Chrome 
# ./install_extension.sh fmkadmapgofadopljbjfkapdkoienihi
