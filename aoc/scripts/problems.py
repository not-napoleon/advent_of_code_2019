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

def process_row(row):
    moves = row.split(",")
    current_point = (0,0,)
    points = {}
    steps = 0
    for move in moves:
        (direction, count) = (move[0], int(str(move[1:])))
        for i in range(count):
            steps += 1
            if direction == "U":
                new_point = (current_point[0], current_point[1]+1)
            elif direction == "D":
                new_point = (current_point[0], current_point[1]-1)
            elif direction == "L":
                new_point = (current_point[0]-1, current_point[1])
            elif direction == "R":
                new_point = (current_point[0]+1, current_point[1])
            else:
                click.echo("Unknown direction %s" % direction)
                exit(1)
            current_point = new_point
            if current_point not in points:
                # good enough, since steps is monotonically increasing
                points[current_point] = steps
    return points

@cli.command()
@click.argument('data', type=click.File('r'))
@click.option("--dist", "taxi_mode", flag_value=True)
@click.option("--score", "taxi_mode", flag_value=False)
def paths(data, taxi_mode):
    rows = data.readlines()
    path1 = process_row(rows[0])
    path2 = process_row(rows[1])
    if len(path2) > len(path1):
        (path1, path2) = (path2, path1)
    best_dist = None
    for point in path1.keys():
        if point in path2:
            if taxi_mode:
                dist = abs(point[0]) + abs(point[1])
            else:
                dist = path1[point] + path2[point]
            if best_dist is None:
                best_dist = dist
            else:
                best_dist = min(best_dist, dist)
    click.echo("Shortest distance to interection: %s" % best_dist)
