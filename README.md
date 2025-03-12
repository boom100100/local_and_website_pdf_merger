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
  - A site may have built-in redirects before the printer prompt opens [ex. print this Indeed page](https://www.indeed.com/jobs?q=sm&l=New+York%2C+NY&from=searchOnHP&vjk=0bf7023a2547e8c8).
  - iframes (not formally tested).
  - Reformatting/excluded content in the printed PDF.

## Setup

    cd /Users/<set-username>/Applications
    git clone https://github.com/boom100100/local_and_website_pdf_merger.git convert_and_combine_pdfs
    cd convert_and_combine_pdfs
        <!-- Optional: symbolically link it to your ideal location. -->

        ln -s  /Users/<set-username>/Applications/convert_and_combine_pdfs /SET/THIS/ABSOLUTE/PATH/convert_and_combine_pdfs

    brew install python@3.13
    brew install python-tk
    brew install pipenv
    pipenv shell
    pipenv install --python 3.13

    cp .env.example .env
    cp -a outputs.example outputs

    <!-- for macos -->
        <!--
            First, set "path" and "allowed origins" in the file com.automatedbooks.convert_and_combine_pdfs.json 
            Then, put the file in the correct directory.
        -->
            cp "/Users/<set-username>/Desktop/github/convert_and_combine_pdfs/com.automatedbooks.convert_and_combine_pdfs.json.macos" "/Users/<set-username>/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.automatedbooks.convert_and_combine_pdfs.json"

        chmod 755 convert_and_combine_pdfs_native_messaging.py

    <!-- for Windows -->
    <!--
        TODO: must fix this. Will need further registry treatment. 
    -->
    cp com.automatedbooks.convert_and_combine_pdfs.json.windows com.automatedbooks.native.messaging.json



## Development
### Changing Dependencies
Only run the following as needed!

Run

    pipenv install dependencyname

to add a new dependency.

Run

    pipenv uninstall dependencyname

to remove a dependency.

Run

    pipenv uninstall --all

to get rid of everything.

Run

    rm Pipfile.lock

to delete Pipfile.lock. 

## Run
CLI commands live in `app/commands`. Call them from the project root directory with the following structure: `flask <app_group_name> <command_name> <flag1> <flag1_arg> <arg1> <arg2> <arg_n>`, e.g. `flask pdf combine -c 2 "https://google.com" "https://google.com/maps" "https://google.com/images"`. Use the `--help` flag to learn about a command's specific options.


## Troubleshooting

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
