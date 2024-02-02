#!/usr/bin/python3
from ansible_vault import Vault
import os
import click
from click_rich_help import StyledGroup
from rich import print
from rich.table import Table
from rich.console import Console
from rich.traceback import install
from getpass import getpass
import pyperclip
install()

def get_vault():
    password_file = os.environ.get("ANSIBLE_VAULT_PASSWORD_FILE")
    password = ''
    if (password_file is not None):
        password = open(password_file).read().rstrip()
    else:
        print("[bold blue]Vault password:[/]")
        password = getpass("")

    if len(password) == 0:
        raise ValueError("Can't use empty password")

    return Vault(password)

@click.group(
    cls=StyledGroup
)
def cli():
    pass


@click.command()
@click.argument("vault_file")
def ls(vault_file: str):
    """only shows names of env varialbes in a given vault file"""
    vault = get_vault()

    console = Console()
    table = Table(show_header=False, header_style="bold red")
    table.add_column("ENV", style="yellow")

    content = vault.load(open(vault_file).read())
    for key in content.keys():
        table.add_row(key)
    
    console.print(table)


@click.command()
@click.argument("vault_file")
def view(vault_file: str):
    """shows names and values of env varialbes in a given vault file"""
    vault = get_vault()
    config = vault.load(open(vault_file).read())

    console = Console()
    table = Table(show_header=False, header_style="bold red")
    table.add_column("ENV", style="yellow")
    table.add_column("value")

    for key, value in config.items():
        table.add_row(key, value)

    console.print(table)

@click.command()
@click.argument("vault_file")
def export(vault_file: str):
    """generates a bash script that exports env variables to parent shell and and removes itself 
    
    copies the command to export to clipboard"""

    vault = get_vault()
    config = vault.load(open(vault_file).read())

    filename = './export.sh'
    with open(filename, 'w') as file:
        file.write("#!/usr/bin/bash\n")

        for key, value in config.items():
            file.write(f"export {key}=\"{value}\"\n")
        
        file.write(f"rm {filename}")
    
    os.chmod(filename, os.stat(filename).st_mode | 0o111)
    pyperclip.copy(f'. {filename}')

@click.command()
@click.argument("vault_file")
def edit(vault_file: str):
    "edit or create new file"
    if os.path.exists(vault_file):
        os.system(f"ansible-vault edit {vault_file}")

    else:
        pass
        os.system(f"$EDITOR {vault_file}")
        os.system(f"ansible-vault encrypt {vault_file}")

cli.add_command(ls)
cli.add_command(view)
cli.add_command(export)
cli.add_command(edit)

if __name__ == "__main__":
    cli()