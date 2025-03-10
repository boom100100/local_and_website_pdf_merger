import base64

import pymupdf
from seleniumbase import SB


from app.services.utils import get_unique_file_name


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
        combined_file_name = get_unique_file_name(output_directory, output_file_name_without_extension_combined)
        combined_file_path = f"{output_directory}/{combined_file_name}"
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
        file_name = f"{output_directory}/{output_file_name}"

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

        with SB(uc=True) as sb:
            sb.activate_cdp_mode(url=webpage_url)
            sb.uc_gui_click_captcha()
            sb.uc_gui_click_cf()
            sb.uc_gui_click_rc()
            sb.sleep(20)
            pdf_data = sb.execute_cdp_cmd("Page.printToPDF", settings)

            file_name = get_unique_file_name(output_directory, output_file_name_without_extension)
            output_path = f"{output_directory}/{file_name}"

        # write pdf to file
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))

        return file_name

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
