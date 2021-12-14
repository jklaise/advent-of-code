from operator import attrgetter
from typing import NamedTuple, List, Literal, Tuple

Char = Literal[0, 1]


class Dot(NamedTuple):
    x: int
    y: int


class Instruction(NamedTuple):
    axis: Literal['x', 'y']
    coord: int


def parse_data(data: List[str]) -> Tuple[List[Dot], List[Instruction]]:
    # dirty imperativeness due to laze
    dots, instructions = [], []
    fold_instruction = 'fold along '
    for line in data:
        if fold_instruction in line:
            instruction = line.strip(fold_instruction)
            axis, coord = instruction.split('=')
            instructions.append(Instruction(axis, int(coord)))
        elif line == '':
            continue
        else:
            x, y = line.split(',')
            dots.append(Dot(int(x), int(y)))

    return dots, instructions


def fold_x(dots: List[Dot], x: int) -> List[Dot]:
    dots = list(filter(lambda dot: dot.x != x, dots))
    max_x = max(dots, key=attrgetter('x')).x
    update_x = lambda dot: Dot(min(dot.x, max_x - dot.x), dot.y)  # assume always fold in the middle
    dots = list(map(update_x, dots))
    dots = list(set(dots))
    return dots


def fold_y(dots: List[Dot], y: int) -> List[Dot]:
    dots = list(filter(lambda dot: dot.y != y, dots))
    max_y = max(dots, key=attrgetter('y')).y
    update_y = lambda dot: Dot(dot.x, min(dot.y, max_y - dot.y))  # assumes always fold in middle
    dots = list(map(update_y, dots))
    dots = list(set(dots))
    return dots


fold_funs = {'x': fold_x, 'y': fold_y}


def apply_instruction(dots: List[Dot], instruction: Instruction) -> List[Dot]:
    fold_fun = fold_funs[instruction.axis]
    return fold_fun(dots, instruction.coord)


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    dots, instructions = parse_data(data)

    # Part 1
    print(f'The answer to part 1 is {len(apply_instruction(dots, instructions[0]))}')
