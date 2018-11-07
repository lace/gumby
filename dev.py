#!/usr/bin/env python

import os
import click
from executor import execute


def nose_cmd():
    # More reliably locate this command when more than one Python are
    # installed.
    try:
        execute("nose2-2.7 --help", capture=True)
        return "nose2-2.7"
    except:
        return "nose2"


def python_source_files():
    import glob

    return glob.glob("*.py") + ["gumby/"]


@click.group()
def cli():
    pass


@cli.command()
def init():
    execute("pip install --upgrade -r requirements_dev.txt")


@cli.command()
def test():
    execute(nose_cmd())


@cli.command()
def lint():
    execute("pyflakes", *python_source_files())


@cli.command()
def black():
    execute("black", *python_source_files())


@cli.command()
def black_check():
    execute("black", "--check", *python_source_files())


@cli.command()
def upload():
    execute("rm -rf dist/")
    execute("python setup.py sdist")
    execute("twine upload dist/*")


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    cli()
