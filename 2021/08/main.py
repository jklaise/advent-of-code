from functools import partial
from operator import itemgetter
from typing import List, Tuple

n_segment_map = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}

inv_n_segment_map = {}
for k, v in n_segment_map.items():
    inv_n_segment_map.setdefault(v, []).append(k)

simple_digits_map = {v[0]: k for k, v in inv_n_segment_map.items() if len(v) == 1}


def parse_line(line: str) -> Tuple[List[str], List[str]]:
    patterns, outputs = line.split(' | ')
    patterns = patterns.split(' ')
    outputs = outputs.split(' ')
    return patterns, outputs


# TODO: typing with generics
def isin(item, collection) -> bool:
    return item in collection


def count_in_collection(items, collection) -> int:
    return sum(map(partial(isin, collection=collection), items))


def outputs_to_lenghts(outputs: List[str]) -> List[int]:
    return list(map(len, outputs))


def part1(data: List[Tuple[List[str], List[str]]]) -> int:
    simple_lenghts = simple_digits_map.values()
    count_in_simple = partial(count_in_collection, collection=simple_lenghts)

    all_outputs = map(itemgetter(1), data)
    all_outputs_lengths = map(outputs_to_lenghts, all_outputs)

    return sum(map(count_in_simple, all_outputs_lengths))


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = list(map(parse_line, data))

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')
