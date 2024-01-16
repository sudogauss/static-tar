import typer
from typing_extensions import Annotated
from typing import List, Tuple, Any
from rich import print as rprint
import os
import subprocess

# CONSTS

PATH_TO_PRESETS="/workspace/musl-cross-make/presets"
PATH_TO_COMPILERS="/workspace/compilers"

cli = typer.Typer()

def get_presets() -> List[str]:
    """
        Gets list of files
    """
    return os.listdir(PATH_TO_PRESETS)

def is_one_of(opts: List[Tuple[Any, Any]]) -> bool:
    found = False
    for (_opt, _default) in opts:
        if _opt != _default:
            if found:
                return False
            found = True

    return True


@cli.command()
def compilers(list: Annotated[bool, typer.Option(help="List all available compiler presets")] = False,
              create: Annotated[str, typer.Option(help="Create a musl cross-compiler from the preset")] = "",
              info: Annotated[str, typer.Option(help="Get info about a preset (prints configuration file)")] = ""):
    """
        Interact with compilers: creation and listing.
    """



    if(list):
        rprint("[bold white]Compiler presets:")
        for preset in get_presets():
            rprint(preset)
        rprint("[/bold white]")
        return
    
    if(info != ""):


@cli.command()
def help():
    """
        Prints help for launcher command
    """

    rprint()
    rprint(f"[bold white]================ Launcher =======================")
    rprint("Usage:")
    rprint("launcher cmd [-cmd_options]")
    rprint()
    rprint("Commands:")
    rprint("    help                                                       Show help note")
    rprint("    compilers [--list] [--create=<preset>] [--info=<preset>]   Manipulate cross compilers")
    rprint("        Details:")
    rprint("            This command allows to list available presets,")
    rprint("            retrieve info about a compiler or create one.")
    rprint("        Options:")
    rprint("            --list                  List all available compiler presets")
    rprint("            --create=<preset>       Create a musl cross-compiler from the preset")
    rprint("            --info=<preset>         Get info about a preset (prints configuration file)")
    rprint("    build --compiler=<preset>")
    rprint("        Details:")
    rprint("            Build standalone tar executable using a preset/compiler")
    rprint("        Options:")
    rprint("            --compiler=<preset>     Choose a compiler to use in order to build tar executable")


def run():
    cli()