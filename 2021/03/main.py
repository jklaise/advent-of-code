from dataclasses import dataclass
from functools import reduce
from itertools import tee
from typing import Callable, Iterable, List, Literal

from toolz.curried import get, peek, peekn


def iterfile(path: str) -> Iterable[str]:
    """
    Utility function to lazily read lines of a file.
    """
    with open(path, 'r') as f:
        yield from f


@dataclass
class BitCounter:
    zeros: int
    ones: int

    # TODO: how to deal with draws not specified
    def most_common(self):
        return '0' if self.zeros > self.ones else '1'

    def least_common(self):
        return '0' if self.zeros <= self.ones else '1'


def create_counters(n: int) -> List[BitCounter]:
    return [BitCounter(0, 0) for _ in range(n)]


def update_count(counter: BitCounter, bit: str) -> BitCounter:
    zeros, ones = counter.zeros, counter.ones
    if bit == '0':
        new_counter = BitCounter(zeros + 1, ones)
    elif bit == '1':
        new_counter = BitCounter(zeros, ones + 1)
    else:
        raise ValueError(f'Unknown bit {bit=}')

    return new_counter


def update_counts(counters: List[BitCounter], bits: str) -> List[BitCounter]:
    return list(map(update_count, counters, bits))


def get_gamma(counters: List[BitCounter]) -> str:
    return ''.join(map(BitCounter.most_common, counters))


def get_epsilon(counters: List[BitCounter]) -> str:
    return ''.join(map(BitCounter.least_common, counters))


def count_bits(bits: Iterable[str]) -> BitCounter:
    return reduce(update_count, bits, BitCounter(0, 0))


def filter_nth(data: Iterable[str], n: int, method: Callable) -> Iterable[str]:
    data_count, data_filter = tee(data)
    bitcounter = count_bits(map(get(n), data_count))
    bit = method(bitcounter)
    return filter(lambda x: x[n] == bit, data_filter)  # (d for d in data if d[n] == bit)


def filter_data(component: Literal['O2', 'CO2'], data: Iterable[str]) -> str:
    if component == 'O2':
        function = BitCounter.most_common
    elif component == 'CO2':
        function = BitCounter.least_common
    else:
        raise ValueError(f'Unknown {component=}')

    n = 0
    peeked, data = peekn(2, data)
    while len(peeked) != 1:
        data = filter_nth(data, n, function)
        peeked, data = peekn(2, data)
        n += 1

    return list(data)[0]


test_data = ['00100',
             '11110',
             '10110',
             '10111',
             '10101',
             '01111',
             '00111',
             '11100',
             '10000',
             '11001',
             '00010',
             '01010']

if __name__ == '__main__':
    # Part 1

    iterlines = iterfile('input.txt')
    first, iterlines = peek(iterlines)
    counters = create_counters(len(first.strip()))  # .strip to remove \n

    final_counters = reduce(update_counts, iterlines, counters)

    gamma = get_gamma(final_counters)
    epsilon = get_epsilon(final_counters)

    print(f'Gamma x Epsilon in decimal: {int(gamma, 2) * int(epsilon, 2)}')

    # Part 2
    iterlines = iterfile('input.txt')
    iterlines_o2, iterlines_co2 = tee(iterlines)

    o2_rating = filter_data(component='O2', data=iterlines_o2)
    co2_rating = filter_data(component='CO2', data=iterlines_co2)

    print(f'O2 x CO2 rating in decimal: {int(o2_rating, 2) * int(co2_rating, 2)}')
