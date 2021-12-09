from functools import partial, reduce
from operator import itemgetter
from string import ascii_letters
from typing import Dict, List, Set, Tuple

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

segment_map = {a: a for a in ascii_letters[:7]}

pattern_to_digit_map = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
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


def outputs_to_lengths(outputs: List[str]) -> List[int]:
    return list(map(len, outputs))


def part1(data: List[Tuple[List[str], List[str]]]) -> int:
    simple_lenghts = simple_digits_map.values()
    count_in_simple = partial(count_in_collection, collection=simple_lenghts)

    all_outputs = map(itemgetter(1), data)
    all_outputs_lengths = map(outputs_to_lengths, all_outputs)

    return sum(map(count_in_simple, all_outputs_lengths))


def create_empty_segment_map() -> Dict[str, str]:
    return dict.fromkeys(segment_map.keys(), None)


def str_sym_diff(a: str, b: str) -> Set[str]:
    return set(a).symmetric_difference(set(b))


def create_segment_mapping(patterns: List[str]) -> Dict[str, str]:
    mapping = create_empty_segment_map()
    lengths = list(map(len, patterns))

    # one has length 2 and seven has length 3, their symmetric diff gives segment a
    one = patterns[lengths.index(2)]
    seven = patterns[lengths.index(3)]
    mapping['a'] = str_sym_diff(one, seven).pop()

    # next, we find four, its sym diff with one gives us possible values for segments b, d
    four = patterns[lengths.index(4)]
    b_d_possible = str_sym_diff(four, one)

    # next, we find two, three and five, their 3 common letters give us possible
    # identities of d, g and a; we can discard a as we already have determined it above
    two_three_five = [set(p) for p in patterns if len(p) == 5]
    a_d_g_possible = reduce(set.intersection, two_three_five)
    d_g_possible = a_d_g_possible.copy()
    d_g_possible.remove(mapping['a'])

    # using the above we can now confirm the identity of d
    mapping['d'] = b_d_possible.intersection(d_g_possible).pop()

    # this also gives us segment b and g
    b_d_possible.remove(mapping['d'])
    mapping['b'] = b_d_possible.pop()

    d_g_possible.remove(mapping['d'])
    mapping['g'] = d_g_possible.pop()

    # symmetric difference of eight and one and all the additional known segments gives us e
    eight = patterns[lengths.index(7)]
    mapping['e'] = (str_sym_diff(eight, one) - set(mapping.values())).pop()

    # finally, identities of c and f can be determined by looking at non-mapped letters
    # of two and five respectively
    adeg = {mapping['a'], mapping['d'], mapping['e'], mapping['g']}
    diffs = list(map(partial(set.symmetric_difference, adeg), two_three_five))
    l_diffs = [len(d) for d in diffs]
    mapping['c'] = diffs[l_diffs.index(1)].pop()
    mapping['f'] = str_sym_diff(one, mapping['c']).pop()

    # NB: we return the reverse mapping as we will be mapping corrupted segments to original ones
    return {v: k for k, v in mapping.items()}


def outputs_to_number(datum: Tuple[List[str], List[str]]) -> int:
    patterns, outputs = datum
    mapping = create_segment_mapping(patterns)

    def convert_output(output: str, mapping) -> str:
        return ''.join(map(mapping.get, output))

    actual_outputs = list(map(partial(convert_output, mapping=mapping), outputs))
    actual_outputs = list(map(lambda x: "".join(sorted(x)), actual_outputs))

    # now create a number
    nums = [str(pattern_to_digit_map[p]) for p in actual_outputs]

    return int("".join(nums))


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = list(map(parse_line, data))

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')

    # Part 2
    numbers = map(outputs_to_number, data)
    print(f'The answer to part 2 is {sum(numbers)}')
