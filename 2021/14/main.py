from collections import Counter
from functools import reduce
from typing import Dict, List, Tuple

from toolz.itertoolz import sliding_window
from toolz.functoolz import compose, curry


def parse_data(data: List[str]) -> Tuple[str, Dict[str, str]]:
    template = data[0]
    rules = {}
    for line in data[2:]:
        pair, insert = line.split(' -> ')
        rules[pair] = insert

    return template, rules


def get_pairs(polymer: str) -> List[str]:
    return list(map("".join, sliding_window(2, polymer)))


def insert(pair: str, insertion: str) -> str:
    return pair[0] + insertion


@curry
def apply_rule(polymer: str, rules: Dict[str, str]) -> str:
    pairs = get_pairs(polymer)
    last = pairs[-1][1]  # keep track of last letter as will need to add it in the end
    insertions = list(map(rules.get, pairs))
    new_pairs = list(map(insert, pairs, insertions))
    return "".join(new_pairs) + last


def part1(data: List[str], steps: int = 10) -> int:
    template, rules = parse_data(data)
    apply_rule_10 = compose(*[apply_rule(rules=rules)] * steps)
    polymer = apply_rule_10(template)
    counts = Counter(polymer).most_common()
    most_common, least_common = counts[0][1], counts[-1][1]
    return most_common - least_common


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')

    # Part2