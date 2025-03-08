import json
import base64
import os

from selenium import webdriver


# TODO: consider functional approach if class requires no attributes.
class Pdf:
    def __init__(self):
        print("instantiated Pdf")

    @staticmethod
    def combine(
        webpage_url: str,
        output_file_name_without_extension: str,
        output_directory: str,
    ):

        print("Downloading webpage.")
        page_pdf_location = Pdf.download_webpage_to_pdf_file(
            webpage_url,
            output_file_name_without_extension,
            output_directory
        )

        print("Combining pdfs.")
        combined_file_name = None # TODO
        existing_file_name = None # TODO
        # TODO: make this accept an arbitrary number of files
        file_locations = [ 
            existing_file_name,
            page_pdf_location
        ]
        Pdf.combine_files(file_locations)

        print("Finished combining.")
        print("See file at:")
        print(combined_file_name)

    @staticmethod
    def download_webpage_to_pdf_file(
        webpage_url,
        output_file_name_without_extension,
        output_directory
    ) -> str:

        # webpage_url = "https://www.google.com/"
        # output_file_name_without_extension = "MyNewName"
        # output_directory = "/Users/bernadette/Downloads"
        output_file_name = f"{output_file_name_without_extension}.pdf"
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

        return output_path

    @staticmethod
    def combine_files(file_locations):
        ...

