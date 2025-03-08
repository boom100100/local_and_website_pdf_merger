import json
import base64
import os

from selenium import webdriver

# // args to set up
  # input webpage URL
  # output file name
  # output directory

webpage_url = "https://www.google.com/"
output_file_name_without_extension = "MyNewName"
output_file_name = f"{output_file_name_without_extension}.pdf"
output_directory = "/Users/bernadette/Downloads"
output_path = f"{output_directory}/{output_file_name}"

settings = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}


profile = {
  'printing.print_preview_sticky_settings.appState': json.dumps(settings),
}

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(webpage_url)

# enabling headless requires alternative to driver.execute_script('window.print();')
pdf_data = driver.execute_cdp_cmd("Page.printToPDF", settings)

# get unique file name
counter = 1
while os.path.isfile(output_path):
    new_output_file_name_without_extension = f"{output_file_name_without_extension} ({counter})"
    output_file_name = f"{new_output_file_name_without_extension}.pdf"
    output_path = f"{output_directory}/{output_file_name}"
    counter += 1

# write pdf to file
with open(output_path, 'wb') as file:
    file.write(base64.b64decode(pdf_data['data']))

driver.close()
