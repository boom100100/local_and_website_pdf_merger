# Local and Website Pdf Merger CLI Tools

## Description

Python CLI tools for merging PDFs. The [ATS Beater](https://github.com/boom100100/ats-beater) (the [Google Chrome extension](https://chromewebstore.google.com/detail/ats-beater/diefpbmcaopdlphclenlgfcmeafacojg)) depends on this CLI app.

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

### MacOs Install Script
Only run one of the two commands below.

Get and install the standalone CLI app with the following command:

    curl https://gist.githubusercontent.com/boom100100/f57dd0460a30bfbe1d920a2d7322d84c/raw/0f59590337cac83addcbb26748f4bfb11f3858ec/install_pdf_combiner.sh | bash

Or, install the CLI app with the native messaging host (if using the Google Chrome extension ATS Beater):

    curl https://gist.githubusercontent.com/boom100100/f57dd0460a30bfbe1d920a2d7322d84c/raw/0f59590337cac83addcbb26748f4bfb11f3858ec/install_pdf_combiner.sh | bash -s 2
<!-- NOTE: if another native messaging host is added, this arg can represent a specific one instead of the script just checking for its presence -->

To enable ATS Beater, restart the Chrome browser so the extension gets installed. Then, in Chrome, select the option to activate the extension when it pops up.


### Windows 
#### Dependencies
Install dependencies:

- [python 3.11.9](https://www.python.org/downloads/release/python-3119/). The Tkinter dependency [should come included](https://tkdocs.com/tutorial/install.html#installwin) in the python installation.
- pipenv

    pip install pipenv
<!-- TODO: must test this setup. -->
<!-- TODO: must script this setup. -->

#### Install Script
After setting up the dependencies, there are two options. Install the standalone CLI app, or install both the ATS Beater extension and the CLI app.

Get and install the standalone CLI app with the following command:

    curl -sO https://gist.githubusercontent.com/boom100100/cb34b92b0b16721309b71eb972c2c010/raw/b3a0ab7b1c90fabebaae93551508b6f2b3d21262/install_app.bat && install_app.bat && del install_app.bat

Or, get and install the CLI app with the native messaging host (if using the Google Chrome extension ATS Beater):

    curl -sO https://gist.githubusercontent.com/boom100100/cb34b92b0b16721309b71eb972c2c010/raw/b3a0ab7b1c90fabebaae93551508b6f2b3d21262/install_app.bat && install_app.bat 1 && del install_app.bat

If using ATS Beater, restart the Chrome browser so the extension gets installed. In Chrome, activate the extension when prompted.


## Development
### Scope
Development needs for this project include the following:

- [ ] Writing end-to-end tests.
- [ ] Writing Uninstallers.
- [x] Windows
  - [x] Writing installation instructions. These will live in a gist that this readme will link to in the setup instructions section.
  - [x] Testing installation. The installation instructions must allow a fresh install to work. And user interactivity must be limited to enabling elevated privileges and uncircumventable manual input requirements within the browser (like enabling the added Chrome extension).
  - [x] UA testing. The cross-platform nature of the project requires testing redundantly while Windows remains less fully developed.

### Process
TBD. For now, open a pull request and tag @boom100100.

## Run
For using the CLI, run `pipenv shell` in the project root directory. All CLI commands must run from that shell.

The CLI commands live in `app/commands`. Call them from the project root directory with the following structure: `flask <app_group_name> <command_name> <flag1> <flag1_arg> <arg1> <arg2> <arg_n>`, e.g. `flask pdf combine -c 2 "https://google.com" "https://google.com/maps" "https://google.com/images"`. 

Use the `--help` flag to learn about a command's specific options, e.g. `flask pdf combine --help`.


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

## Learnings
- Yoshi is born wearing boots and a saddle. (It's probably not a shell, as Yoshi is a dinosaur/dragon, not a koopa.)
- Female dinosaurs lay eggs. As for Yoshi and Birdo's gender... have they ever been asked about that identity? There are so many opinions.
- Is Mario punching Yoshi on the back of the head, or... ? Oh, he's *pointing*. And Yoshi can see that somehow.
