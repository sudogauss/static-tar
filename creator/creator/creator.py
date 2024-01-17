import typer
from typing_extensions import Annotated
from typing import List, Tuple, Any
from rich import print as rprint
import os
import sys
import shutil
import subprocess

# CONSTS

PATH_TO_CROSS_MAKE="/workspace/musl-cross-make"
PATH_TO_PRESETS="/workspace/musl-cross-make/presets"
PATH_TO_COMPILERS="/workspace/compilers"

cli = typer.Typer()

def __get_presets() -> List[str]:
    """
        Get list of presets contained in musl cross-compilers presets
    """
    return os.listdir(PATH_TO_PRESETS)

def __is_one_of(opts: List[Tuple[Any, Any]]) -> bool:
    """
        Checks if only one option is applied at a time
    """
    found = False
    for (_opt, _default) in opts:
        if _opt != _default:
            if found:
                return False
            found = True

    return True

def __print_preset_info(preset: str) -> None:
    """
        Prints the content of compiler configuration preset file.
    """
    _path = PATH_TO_PRESETS + "/" + preset
    rprint("[bold green]Preset " + preset + " info:[/bold green]")
    with open(_path, 'r') as stream:
        for line in stream.readlines():
            if "#" not in line:
                rprint(line)

def __build_compiler(compiler: str) -> None:
    """
        Builds chosen musl based cross-compilation toolchain.
    """
    src = PATH_TO_PRESETS + "/" + compiler
    dst = PATH_TO_CROSS_MAKE + "/config.mak"
    shutil.copy(src, dst)
    proc = subprocess.Popen(["make", "-j20", "install"], text=True, cwd=PATH_TO_CROSS_MAKE, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        line_ = str(line)
        if len(line_) > 1:
            sys.stdout.write(str(line))


@cli.command()
def compilers(list: Annotated[bool, typer.Option(help="List all available compiler presets")] = False,
              create: Annotated[str, typer.Option(help="Create a musl cross-compiler from the preset")] = "",
              info: Annotated[str, typer.Option(help="Get info about a preset (prints configuration file)")] = ""):
    """
        Interact with compilers: creation and listing.
    """

    if not __is_one_of([(list, False), (create, ""), (info, "")]):
        rprint("[bold red]Only one of options must be applied at a time.[/bold red]")

    if(list):
        rprint("[bold white]Compiler presets:[/bold white]")
        for preset in __get_presets():
            rprint(preset)
        rprint()
        return
    
    if(info != ""):
        _presets = __get_presets()
        if info in _presets:
            __print_preset_info(info)
        else:
            rprint("[bold red]The following preset is not available: " + info + "[/bold red]")

    if(create != ""):
        _presets = __get_presets()
        if create in _presets:
            __build_compiler(create)
        else:
            rprint("[bold red]The following preset is not available: " + info + "[/bold red]")


@cli.command()
def build(compiler: Annotated[str, typer.Option(help="Choose a compiler to build tar")] = ""):
    """
        Allows to build static tar executable with chosen compiler.
    """

    if compiler == "":
        rprint("[bold red]Error: you must provide compiler to build to tar with[/bold red]")
        return

    _compiler = PATH_TO_COMPILERS + "/" + compiler
    if not os.path.isdir(_compiler):
        rprint("[bold red]Error: compiler " + compiler + " does not exist[/bold red]")

    


def run():
    cli()