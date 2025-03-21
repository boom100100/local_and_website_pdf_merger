# Local and Website Pdf Merger CLI Tools

## Description

Python CLI tools for merging PDFs.

Features
- Combine PDF files from the local computer.
- Convert webpages to PDF and combine them.
- Environment variables can be set to select files, webpages, and the output directory for serial usage.
- Automatically delete downloaded files.
- Automatically open the combined file.

This project won't support:

- Reordering webpage download files in front of local files. Chosen local files will always be merged in front of files downloaded from the Internet. The workaround for this is 1) to run the tool to download webpage files locally, and then 2) re-run the tool to select each local file to merge in the ideal order.
- Selecting individual pages or changing their order.
- Fixing site-specific idiosyncracies.
  - YMMV with the captcha handling.
  - Handling built-in redirects a site may have set up before the printer prompt opens [ex. print this Indeed page](https://www.indeed.com/jobs?q=sm&l=New+York%2C+NY&from=searchOnHP&vjk=0bf7023a2547e8c8).
  - iframes (not formally tested).
  - Reformatting/excluded content in the printed PDF.

## Setup

Setup requires downloading the project and its dependencies.

### MacOs

#### Installer
Install with the native messaging host (if using Google Chrome extension ATS Beater):

    curl https://gist.githubusercontent.com/boom100100/f57dd0460a30bfbe1d920a2d7322d84c/raw/e894d4db0c6c259eafe8ce7b5a12942461127808/install_pdf_combiner.sh | bash -s 2

After running this command, restart Chrome and select the option to activate the extension.

Install without the native messaging host:

    curl https://gist.githubusercontent.com/boom100100/f57dd0460a30bfbe1d920a2d7322d84c/raw/e894d4db0c6c259eafe8ce7b5a12942461127808/install_pdf_combiner.sh | bash

#### Manually Install

Install dependencies:

    brew install python@3.13
    brew install python-tk
    brew install pipenv

Get the app:

    cd ~/Applications
    git clone https://github.com/boom100100/local_and_website_pdf_merger.git convert_and_combine_pdfs

Configure the app:

    cd convert_and_combine_pdfs
    cp .env.example .env
    cp -a outputs.example outputs

        <!-- Optional: symbolically link it to your ideal location. -->

        ln -s  ~/Applications/convert_and_combine_pdfs /SET/THIS/ABSOLUTE/PATH/convert_and_combine_pdfs

    mkdir .venv
    pipenv shell
    pipenv install --python 3.13

Configure the native host (if using Google Chrome extension ATS Beater):

    chmod 755 install_host.sh
    ./install_host.sh

Now, restart Chrome so the extension gets installed. Select the option to activate the extension from the web browser.

### Windows
For Windows, manual and installer setup is within scope for future development (but development start date undetermined).
<!-- #### Installer TODO -->
#### Manually Install
<!-- TODO: must test this setup. -->
<!-- TODO: must script this setup. -->
Install dependencies:

- [python 3.13.2](https://www.python.org/downloads/release/python-3132/). The Tkinter dependency [should come included](https://tkdocs.com/tutorial/install.html#installwin) in the python installation.
- pipenv

    pip install pipenv

Get the app:

    cd "C:\\Program Files"
    git clone https://github.com/boom100100/local_and_website_pdf_merger.git convert_and_combine_pdfs
    cd convert_and_combine_pdfs

Configure the app:

    cp .env.example .env
    cp -a outputs.example outputs

    mkdir .venv
    pipenv shell
    pipenv install --python 3.13
    sbase get uc_driver

Configure the native host (if using Google Chrome extension ATS Beater):

    install_host.bat

And then restart Chrome so the extension gets installed. Select the option to activate the extension from the web browser.


## Development
### Scope
Development needs for this project include the following:

- Writing end-to-end tests.
- Writing Uninstallers.
- Windows
  - Writing installation instructions. These will live in a gist that this readme will link to in the setup instructions section.
  - Testing installation. The installation instructions must allow a fresh install to work. And user interactivity must be limited to enabling elevated privileges and uncircumventable manual input requirements within the browser (like enabling the added Chrome extension).
  - UA testing. The cross-platform nature of the project requires testing redundantly while Windows remains less fully developed.

### Process
TBD. For now, open a pull request and tag @boom100100.

## Run
CLI commands live in `app/commands`. Call them from the project root directory with the following structure: `flask <app_group_name> <command_name> <flag1> <flag1_arg> <arg1> <arg2> <arg_n>`, e.g. `flask pdf combine -c 2 "https://google.com" "https://google.com/maps" "https://google.com/images"`. Use the `--help` flag to learn about a command's specific options.


## Troubleshooting

### Webpage Won't Download
If the app, native host, and extension all appear to install correctly, but the app fails at the step of downloading the webpage as a PDF, then make sure `.env` has the environmental variable `SE_CHROMEDRIVER`.

### Json file with wrong extension

    sudo rm "/Library/Google/Chrome/NativeMessagingHosts/com.automatedbooks.convert_and_combine_pdfs.json-e"


### Shell Doesn't Recognize Dependencies

In some sytem states, the Pipenv shell may not recognize dependencies after they were installed. One such case is when running `deactivate` while in the shell:

> `> deactivate`
> `> pipenv shell`
> Loading .env environment variables...
> Shell for UNKNOWN_VIRTUAL_ENVIRONMENT already activated.
> New shell not activated to avoid nested environments.
> `> flask --version`
> zsh: command not found: flask

Run `exit` instead of `deactivate`.

In any case (e.g. even if `deactivate` *is* accidentally used), just exit and reenter the shell as usual:

```
exit 
pipenv shell
flask --version
```
