""" Test the ansible-role Cookiecutter template.

A template project is created in a temporary directory, and the role's test
suite is run using molecule in a virtualenv environment.

"""
from cookiecutter.main import cookiecutter
from json import load
from os import chdir
from pathlib import Path
from shlex import split
from subprocess import check_call
from tempfile import TemporaryDirectory
from venv import create


def main() -> int:
    """ Execute the test.
    
    """
    def pymod(command: str):
        """ Run a Python module inside the virtual environment. """
        check_call(split(f"python -m {command:s}"))
        return

    template = Path(__file__).resolve().parents[1]
    defaults = load(Path(template, "cookiecutter.json").open("rt"))
    with TemporaryDirectory() as tmpdir:
        chdir(tmpdir)
        cookiecutter(str(template), no_input=True)
        chdir(defaults["project_slug"])
        venv = Path(".venv")
        create(venv, with_pip=True)
        pymod("pip install -r molecule/requirements.txt")
        pymod("molecule test")
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    exit(main())
