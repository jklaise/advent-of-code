from dataclasses import dataclass
from functools import reduce
from typing import Iterable, List


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

    # TODO: how to determine the length of the line without consuming
    #  from the lazy generator?
    n_length = 12
    counters = create_counters(12)

    iterlines = iterfile('input.txt')
    final_counters = reduce(update_counts, iterlines, counters)

    gamma = get_gamma(final_counters)
    epsilon = get_epsilon(final_counters)

    print(f'Gamma x Epsilon in decimal: {int(gamma, 2) * int(epsilon, 2)}')
