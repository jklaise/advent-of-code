from collections import Counter
from functools import reduce
from typing import List

test_data = [3, 4, 3, 1, 2]


def compose(f1, f2):
    return f2(f1)


def update_fish(fish: int) -> int:
    if fish > 0:
        return fish - 1
    elif fish == 0:
        return 6


def update_state(state: List[int]) -> List[int]:
    numzero = Counter(state)[0]  # inefficient to do every time
    state = list(map(update_fish, state))
    state.extend([8] * numzero)
    return state


def update_counts(counter: Counter) -> Counter:
    new_counter = Counter()
    for lifetime, number in counter.items():
        if lifetime == 0:
            new_counter[8] += number
            new_counter[6] += number
        else:
            new_counter[lifetime - 1] += number
    return new_counter


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().strip().split(',')
    data = [int(d) for d in data]

    # Part 1
    N_DAYS = 80
    result = reduce(compose, [data, *[update_state] * N_DAYS])
    print(f'Answer to part 1 is {len(result)}')

    # Part 2
    N_DAYS = 256
    counter = Counter(data)
    result = reduce(compose, [counter, *[update_counts] * N_DAYS])
    print(f'Answer to part 2 is {sum(result.values())}')
