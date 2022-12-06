import itertools
from typing import Iterable, Iterator


def sliding_window(iterable: Iterable, n: int) -> Iterator:
    iterables = itertools.tee(iterable, n)

    for iterable, num_skipped in zip(iterables, itertools.count()):
        for _ in range(num_skipped):
            next(iterable, None)

    return zip(*iterables)


def get_position(buffer: str, n: int) -> int:
    window_of_n = sliding_window(buffer, n=n)
    index = -1
    chars = set()
    while len(chars) != n:
        index += 1
        chars = set(next(window_of_n))
    return index + n


if __name__ == "__main__":
    with open('input.txt') as f:
        buffer = f.read().strip()

    # Part 1
    position = get_position(buffer, n=4)
    print(position)

    # Part 2
    position = get_position(buffer, n=14)
    print(position)
