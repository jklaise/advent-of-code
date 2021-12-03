from toolz.dicttoolz import valmap
from toolz.itertoolz import groupby
from operator import itemgetter


def part1(instructions: map) -> int:
    # group by key
    gb = groupby(lambda x: x[0], instructions)

    # map over values a function which gets the numbers and sums them up
    value_summer = lambda x: sum(map(itemgetter(1), x))
    sums = valmap(value_summer, gb)

    # final result
    forward = sums['forward']
    depth = sums['down'] - sums['up']

    return forward * depth


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = map(str.split, f.readlines())
        instructions = map(lambda x: (x[0], int(x[1])), instructions)  # convert str to int

    print(part1(instructions))
