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
    click.echo("Total is %s" % total)

@cli.command()
@click.argument('data', type=click.File('r'))
def intcode(data):
    raw = data.read().replace("\n", "")
    program = [int(value) for value in raw.split(",")]
    op_ptr = 0
    while program[op_ptr] != 99:
        (op, in_1, in_2, out) = program[op_ptr:op_ptr+4]
        if op == 1:
            program[out] = program[in_1] + program[in_2]
        elif op == 2:
            program[out] = program[in_1] * program[in_2]
        elif op == 99:
            # not sure how this happened, but fine
            break
        else:
            click.echo("Invalid op at %s, current state is \n%s" % (op_ptr, program))
            exit(1)
        op_ptr += 4
    click.echo("Position 0: %s" % program[0])
    click.echo("Final state: %s" % program)
