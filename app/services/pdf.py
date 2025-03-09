import json
import base64

from app.services.utils import get_unique_file_name
import pymupdf
from selenium import webdriver


# TODO: consider functional approach if class requires no attributes.
class Pdf:
    def __init__(self):
        print("instantiated Pdf")

    @staticmethod
    def combine(
        existing_file_paths: list[str],
        webpage_urls: tuple[str, ...],
        output_file_name_without_extension: str,
        output_directory: str,
    ) -> None:
        # TODO: enable reordering. All existing will always be before all webpage downloads.
        file_locations = existing_file_paths
        
        if webpage_urls:
            print("Downloading webpage(s).")

        for webpage_url in webpage_urls:
            webpage_pdf_file_path = Pdf.download_webpage_to_pdf_file(
                webpage_url,
                output_file_name_without_extension,
                output_directory
            )
            file_locations.append(webpage_pdf_file_path)

        if len(file_locations) == 0:
            print("There are no files to combine.")
            print("\nEnding process early.")
            return

        if len(file_locations) == 1:
            print("There is only one file to combine:\n")
            print(file_locations[0])
            print("\nEnding process early.")
            return

        print("Combining pdfs.")
        output_file_name_without_extension_combined = f"{output_file_name_without_extension} combined"
        combined_file_path = get_unique_file_name(output_directory, output_file_name_without_extension_combined)
        Pdf.combine_files(combined_file_path, file_locations)

        print("Finished combining.")
        print("See file at:")
        print(combined_file_path)


    @staticmethod
    def download_webpage_to_pdf_file(
        webpage_url: str,
        output_file_name_without_extension: str,
        output_directory: str
    ) -> str:
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

        output_path = get_unique_file_name(output_directory, output_file_name_without_extension)
        # # get unique file name
        # counter = 1
        # while os.path.isfile(output_path):
        #     new_output_file_name_without_extension = f"{output_file_name_without_extension} ({counter})"
        #     output_file_name = f"{new_output_file_name_without_extension}.pdf"
        #     output_path = f"{output_directory}/{output_file_name}"
        #     counter += 1

        # write pdf to file
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))

        driver.close()

        return output_path

    @staticmethod
    def combine_files(
        combined_file_path: str,
        file_locations: list[str]
    ) -> None:
        pdfs = [
            pymupdf.open(file_location)
            for file_location in file_locations
        ]
        first_pdf = pdfs.pop(0)
        for pdf in pdfs:
            first_pdf.insert_pdf(pdf)

        first_pdf.save(combined_file_path)
