# Local and Website Pdf Merger CLI Tools

## Description

Python CLI tools for merging PDFs. For now, this project won't support:

- Reordering webpage download files in front of local files. Chosen local files will always be merged in front of files downloaded from the web. The workaround for this is 1) to run the tool to download webpage files locally, and then 2) re-run the tool to select each local file to merge in the ideal order.
- Selecting individual pages or changing their order.

## Setup

    cd projectDir
    brew install python@3.13
    brew install python-tk

### Pipenv

    brew install pipenv
    pipenv shell
    pipenv install --python 3.13


## Changing Dependencies
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
Run the following from the project's root directory:

    flask run --debug

## Add new CLI commands

CLI commands live in `app/commands`. Call them with the following structure: `flask <app_group_name> <command_name> <flag1> <flag1_arg> <arg1> <arg2> <arg_n>`, e.g. `flask pdf combine -c 2 "https://google.com" "https://google.com/maps" "https://google.com/images"`.


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
