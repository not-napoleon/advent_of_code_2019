"""
Scripts for solving specific problems
"""
import click

from tqdm import tqdm

def comp_intcode(program, noun, verb):
    program = program.copy()
    program[1] = noun
    program[2] = verb
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
    return program[0]

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
    with tqdm(total=99*99) as pbar:
        for i in range(99):
            for j in range(99):
                output = comp_intcode(program, i, j)
                if output == 19690720:
                    break
                pbar.update(1)
            if output == 19690720:
                break
    click.echo("noun: %s, verb: %s, answer: %s" % (i, j, 100 * i + j))
