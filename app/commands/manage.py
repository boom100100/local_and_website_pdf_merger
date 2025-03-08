from app.commands.pdf_group.combine import pdf_cli

command_groups = [
    pdf_cli,
]

def add_commands(app):
    for command_group in command_groups:
        app.cli.add_command(command_group)
