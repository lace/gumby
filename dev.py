#!/usr/bin/env python2

import click
from executor import execute

@click.group()
def cli():
    pass

@cli.command()
def init():
    execute('pip install -r requirements_dev.txt')

@cli.command()
def test():
    execute('nose2')

if __name__ == '__main__':
    cli()
