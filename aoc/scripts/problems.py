"""
Scripts for solving specific problems
"""
import click

from tqdm import tqdm

@click.group()
def cli():
    """Example Command Script"""

@cli.command()
@click.argument('data', type=click.File('rb'))
@click.option("--recurse/--no-recurse", default=False)
def fuel(data, recurse):
    total = 0
    for value in tqdm(data):
        value = int(value)
        fuel_increment = (value // 3) - 2
        if recurse:
            while fuel_increment > 0:
                total += fuel_increment
                fuel_increment = (fuel_increment // 3) -2
        else:
            total += fuel_increment
    print("Total is %s" % total)
