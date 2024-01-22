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
PATH_TO_TAR="/workspace/tar"
PATH_TO_TAR_OUTPUT="/workspace/tars"

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

def __process_cmd(cmd, cwd: str) -> None:
    """
        Runs a subprocess executing provided command and returns output/stderr line by line
    """
    proc = subprocess.Popen(cmd, cwd=cwd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:

        finished_ = proc.poll()
        line = proc.stdout.readline()
        line_ = str(line)
        if len(line_) > 1:
            yield line_

        if finished_ is not None:
            break


def __build_compiler(compiler: str) -> None:
    """
        Builds chosen musl based cross-compilation toolchain.
    """
    src = PATH_TO_PRESETS + "/" + compiler
    dst = PATH_TO_CROSS_MAKE + "/config.mak"
    shutil.copy(src, dst) # Copy compiler config preset and rename it to config.mak
    for out in __process_cmd(["make", "-j20", "install"], PATH_TO_CROSS_MAKE): # Running make install for configured compiler
        print(out)


def __build_tar(compiler: str) -> None:
    """
        Builds a standalone tar binary using provided compiler.
    """

    compiler_dir_ = PATH_TO_COMPILERS + "/" + compiler
    compiler_executable_ = compiler_dir_ + "/bin/" + compiler + "-gcc"
    compiler_include_path_ = compiler_dir_ + "/" + compiler + "/include"
    compiler_lib_path_ = compiler_dir_ + "/" + compiler + "/lib"

    if not os.path.isdir(compiler_dir_):
        rprint("[bold red]Error: compiler does not exist[/bold red]")

    for out in __process_cmd(["./bootstrap"], PATH_TO_TAR): # Bootstrap tar automake system
        print(out)

    output_ = PATH_TO_TAR_OUTPUT + "/" + compiler + "-tar"
    cc = "CC=" + compiler_executable_
    ld_flags = "LDFLAGS=-static -L" + compiler_lib_path_
    cpp_flags = "CPPFLAGS=-I" + compiler_include_path_

    for out in __process_cmd(["./configure", "--prefix", output_, cc, ld_flags, cpp_flags], PATH_TO_TAR):
        print(out)

    for out in __process_cmd(["make", "-j20", "install"], PATH_TO_TAR):
        print(out)



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

    __build_tar(compiler)    


def run():
    cli()