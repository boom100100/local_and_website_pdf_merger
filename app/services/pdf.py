import json
import base64

import pymupdf
from selenium import webdriver

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


        # profile = {
        # 'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        # }

        # chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_experimental_option('prefs', profile)
        # chrome_options.add_argument('--kiosk-printing')
        # chrome_options.add_argument("--headless")

        # driver = webdriver.Chrome(options=chrome_options)
        # waitTime = 30
        # driver.implicitly_wait(waitTime)
        # driver.get(webpage_url)

        # enabling headless requires alternative to driver.execute_script('window.print();')
        # pdf_data = driver.execute_cdp_cmd("Page.printToPDF", settings)
        # pdf_data = None

        # with SB() as sb:
        # with SB(uc=True, test=True) as sb:
        with SB(uc=True) as sb:
            # sb.activate_cdp_mode(url=webpage_url)
            # sb.sleep(10)
            # sb.get_element("iframe", by="css selector")
            # sb.switch_to_frame("iframe")
            # sb.uc_gui_click_captcha()
            # sb.cdp.gui_click_element("input[type=checkbox]")
            # sb.click("input[type=checkbox]", by="css selector", timeout=None, delay=0, scroll=True)

            # # sb.uc_open(webpage_url)
            # sb.switch_to_default_content()
            # # sb.uc_open("https://google.com")
            # # sb.uc_open_with_reconnect(webpage_url)
            # # # sb.uc_open(webpage_url)
            # # sb.save_cookies(name="cookies.txt")
            # # sb.uc_open("https://google.com/maps")
            # # sb.uc_open("https://google.com/shopping")
            # # sb.uc_open("https://google.com/images")
            # # sb.uc_open_with_reconnect(webpage_url)
            # # sb.uc_gui_click_captcha()
            # # sb.uc_open_with_disconnect(webpage_url)
            # # sb.uc_gui_handle_captcha()
            # # sb.uc_open_with_disconnect(webpage_url, timeout=1)
            # # sb.sleep(180)
            # # sb.switch_to_frame()
            # # sb.cdp.gui_click_element("input[type=checkbox]")
            # # sb.sleep(180)
            # # sb.uc_gui_click_captcha()
            # # sb.uc_gui_click_captcha()
            # # sb.sleep(180)
            # # sb.cdp.gui_click_element("#turnstile-widget div")
        # # with SB(uc=True) as sb:
        #     sb.activate_cdp_mode(url=webpage_url)
        #     # sb.uc_open_with_reconnect(webpage_url)
            sb.activate_cdp_mode()
            sb.open(webpage_url)
            sb.uc_gui_click_captcha()
        #     sb.sleep(4)
            # sb.uc_gui_handle_captcha()
            # pdf_data = driver.execute_cdp_cmd("Page.printToPDF", settings)
            pdf_data = sb.execute_cdp_cmd("Page.printToPDF", settings)
            # write pdf to file
            output_path = get_unique_file_name(output_directory, output_file_name_without_extension)
            # output_file_name = output_path.strip(f"{output_directory}/")

            # sb.save_data_as(pdf_data, output_file_name, destination_folder=output_directory)


        # write pdf to file
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))

        # driver.close()

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
