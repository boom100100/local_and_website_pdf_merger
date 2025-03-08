import click

from app.commands.groups import pdf_cli
from app.services import Pdf


# call this CLI command as `flask user create <name> <name2>`:
# flask user create awes awes2
@pdf_cli.command('combine') # the string value here represents the command_name
# choose whatever name you want for these arguments. 
# They map ordered to the function parameter names.
# Two args need two parameters, etc.
@click.argument('webpage_url')
@click.argument('output_file_name_without_extension')
@click.argument('output_directory') 
# TODO:
# function name structure: verb_object
# and use the same name for argument mapping so it's not confusing
def combine_pdfs(
    webpage_url,
    output_file_name_without_extension,
    output_directory
): 
    Pdf.combine(
        webpage_url,
        output_file_name_without_extension,
        output_directory
    )