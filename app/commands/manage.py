from app.commands.user_group import pdf_cli

command_groups = [
    pdf_cli,
]

def add_commands(app):
    for command_group in command_groups:
        app.cli.add_command(command_group)
