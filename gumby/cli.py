"""
python3 -m gumby.cli landmarks examples/vitra/vitra.yml
python3 -m gumby.cli run examples/vitra/vitra.yml stretched.obj
"""

import click
from .recipe import Recipe


@click.group()
def cli():
    pass


@cli.command()
@click.argument("recipe")
def landmarks(recipe):
    """
    Print the landmarks for the recipe in the YAML file RECIPE.
    """
    from .landmarks import print_landmarks

    recipe_obj = Recipe.load(recipe)
    print_landmarks(recipe_obj.landmarks)


@cli.command()
@click.argument("recipe")
@click.argument("output_path")
def run(recipe, output_path):
    """
    Run the recipe in the YAML file RECIPE and writes it to OUTPUT_PATH.
    """
    recipe_obj = Recipe.load(recipe)
    mesh = recipe_obj.run()
    mesh.write_obj(output_path)


if __name__ == "__main__":
    cli()
