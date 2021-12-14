from collections import Counter
from typing import Dict, Iterable, List, Tuple

from toolz.itertoolz import sliding_window
from toolz.functoolz import compose, curry


def parse_data(data: List[str]) -> Tuple[str, Dict[str, str]]:
    template = data[0]
    rules = {}
    for line in data[2:]:
        pair, insert = line.split(' -> ')
        rules[pair] = insert

    return template, rules


def get_pairs(polymer: str) -> Iterable[str]:
    return map("".join, sliding_window(2, polymer))


def insert(pair: str, insertion: str) -> str:
    return pair[0] + insertion


@curry
def apply_rule(polymer: str, rules: Dict[str, str]) -> str:
    pairs = list(get_pairs(polymer))
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


#### Part 2 functions
def make_new_pair_dict(rules: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
    return {k: (k[0] + v, v + k[1]) for k, v in rules.items()}


def get_new_letters_counter(pair_counter: Counter, rules: Dict[str, str]) -> Counter:
    letter_counter = Counter()
    for pair, count in pair_counter.items():
        letter_counter.update({rules[pair]: count})
    return letter_counter


def get_new_pairs_counter(pair_counter: Counter, pairs_dict: Dict[str, Tuple[str, str]]) -> Counter:
    new_pair_counter = Counter()
    for pair, count in pair_counter.items():
        new0, new1 = pairs_dict[pair]
        new_pair_counter.update({new0: count, new1: count})
    return new_pair_counter


def part2(data: List[str], steps: int = 40) -> int:
    template, rules = parse_data(data)
    pairs_dict = make_new_pair_dict(rules)  # 'CN' : ('CC', 'NC')
    pairs = get_pairs(template)
    letter_counter = Counter(template)
    pair_counter = Counter(pairs)
    for step in range(steps):
        new_letters = get_new_letters_counter(pair_counter, rules)
        pair_counter = get_new_pairs_counter(pair_counter, pairs_dict)  # pair counter is fresh
        letter_counter.update(new_letters)  # letter counter gets updates

    counts = letter_counter.most_common()
    most_common, least_common = counts[0][1], counts[-1][1]
    return most_common - least_common


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')

    # Part2
    print(f'The answer to part 2 is {part2(data)}')
