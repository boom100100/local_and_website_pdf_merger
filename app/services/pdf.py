import base64

import pymupdf
from seleniumbase import SB


from app.services.utils import delete_files, get_unique_file_name, open_file


class Pdf:
    def __init__(
        self,
        existing_file_paths: list[str],
        webpage_urls: list[str],
        output_file_name_without_extension: str, 
        output_directory: str,
        should_open_output_file: bool,
        should_delete_downloaded_files: bool,
    ) -> None:
        self.existing_file_paths = existing_file_paths
        self.webpage_urls = webpage_urls
        self.output_file_name_without_extension = output_file_name_without_extension
        self.output_directory = output_directory
        self.should_open_output_file = should_open_output_file
        self.should_delete_downloaded_files = should_delete_downloaded_files


    def combine(self) -> None:
        file_locations = self.existing_file_paths
        file_locations_for_deletion = []

        
        if self.webpage_urls:
            print("Downloading webpage(s).")

        for webpage_url in self.webpage_urls:
            webpage_pdf_file_path = self.download_webpage_to_pdf_file(
                webpage_url,
            )
            file_locations.append(webpage_pdf_file_path)
            file_locations_for_deletion.append(webpage_pdf_file_path)

        if len(file_locations) == 0:
            print("There are no files to combine.")
            print("\nEnding process early.")
            return

        if len(file_locations) == 1:
            print(f"""There is only one file to combine:

{file_locations[0]}

{'This file will not be deleted in this process.\n\n' if file_locations_for_deletion and self.should_open_output_file and self.should_delete_downloaded_files else ''}Ending process early.""")
            open_file(file_locations[0], self.should_open_output_file)
            should_delete_edge_case = self.should_delete_downloaded_files and not self.should_open_output_file
            delete_files(file_locations_for_deletion, should_delete_edge_case)
            return

        print("Combining pdfs.")
        output_file_name_without_extension_combined = f"{self.output_file_name_without_extension} combined"
        combined_file_name = get_unique_file_name(self.output_directory, output_file_name_without_extension_combined)
        combined_file_path = f"{self.output_directory}/{combined_file_name}"
        Pdf.combine_files(combined_file_path, file_locations)

        print(f"""Finished combining.
See file at:

{combined_file_path}
""")
        open_file(combined_file_path, self.should_open_output_file)
        delete_files(file_locations_for_deletion, self.should_delete_downloaded_files)



    def download_webpage_to_pdf_file(
        self,
        webpage_url: str,
    ) -> str:
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
            # sb.uc_gui_click_cf()
            # sb.uc_gui_click_rc()
            # TODO: there are some issues with indeed.com redirecting upon opening the print dialog.
                # Consider capturing html and converting to PDF instead of printing to PDF.
            # onbeforeunload = (event) => {event.preventDefault();};
            pdf_data = sb.execute_cdp_cmd("Page.printToPDF", settings)

        output_file_name = get_unique_file_name(self.output_directory, self.output_file_name_without_extension)
        output_path = f"{self.output_directory}/{output_file_name}"

        # write pdf to file
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))

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
