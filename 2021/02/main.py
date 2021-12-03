from functools import reduce
from operator import itemgetter
from typing import Iterable, NamedTuple

from toolz.dicttoolz import valmap
from toolz.itertoolz import groupby


def part1(instructions: Iterable) -> int:
    """
    The order of instructions doesn't matter so we can
    get away with using groupby.
    """
    # group by key
    gb = groupby(lambda x: x[0], instructions)

    # map over values a function which gets the numbers and sums them up
    value_summer = lambda x: sum(map(itemgetter(1), x))
    sums = valmap(value_summer, gb)

    # final result
    forward = sums['forward']
    depth = sums['down'] - sums['up']

    return forward * depth


def iterfile(path: str):
    """
    Utility function to lazily read lines of a file.
    """
    with open(path, 'r') as f:
        yield from f


Command = NamedTuple('Command', [('direction', str), ('value', int)])
Position = NamedTuple('Position', [('horizontal', int), ('depth', int)])
State = NamedTuple('State', [('aim', int), ('position', Position)])  # for part 2


def parse_data(raw_data: Iterable[str]) -> Iterable[Command]:
    return (Command(direction, int(value)) for direction, value in map(str.split, raw_data))


def update_position(position: Position, command: Command) -> Position:
    name, value = command
    forward, depth = position
    if name == 'forward':
        new_position = Position(forward + value, depth)
    elif name == 'down':
        new_position = Position(forward, depth + value)
    elif name == 'up':
        new_position = Position(forward, depth - value)
    else:
        raise ValueError(f'Unknown command {name=}.')

    return new_position


def update_state(state: State, command: Command) -> State:
    name, value = command
    aim, (horizontal, depth) = state
    if name == 'forward':
        new_state = State(aim=aim, position=Position(horizontal=horizontal + value, depth=depth + aim * value))
    elif name == 'down':
        new_state = State(aim=aim + value, position=Position(horizontal, depth))
    elif name == 'up':
        new_state = State(aim=aim - value, position=Position(horizontal, depth))
    else:
        raise ValueError(f'Unknown command {name=}.')

    return new_state


if __name__ == '__main__':
    # read everything in memory
    with open('input.txt') as f:
        commands = map(str.split, f.readlines())
        commands = map(lambda x: (x[0], int(x[1])), commands)  # convert str to int

    # groupby part 1
    print(f'Answer to Part 1 using groubpy is {part1(commands)}')

    # lazy read
    iterlines = iterfile('input.txt')
    commands = parse_data(iterlines)

    # reduce part 1
    initial_position = Position(0, 0)
    final_position = reduce(update_position, commands, initial_position)
    print(f'Answer to Part 1 using reduce and lazy iteration is '
          f'{final_position.horizontal * final_position.depth}')

    # lazy read
    iterlines = iterfile('input.txt')
    commands = parse_data(iterlines)

    # reduce part2
    initial_state = State(aim=0, position=Position(0, 0))
    final_state = reduce(update_state, commands, initial_state)
    final_position = final_state.position
    print(f'Answer to Part 2 using reduce and lazy iteration is '
          f'{final_position.horizontal * final_position.depth}')
