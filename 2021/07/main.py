from functools import partial
from typing import Callable, List, Tuple

test_data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def fuel_cost(initial_pos: int, aligned_pos: int) -> int:
    return abs(initial_pos - aligned_pos)


def fuel_cost_part2(initial_pos: int, aligned_pos: int) -> int:
    n_moves = abs(initial_pos - aligned_pos)
    cost = int(n_moves * (n_moves + 1) / 2)
    return cost


def total_fuel_cost(aligned_pos: int, initial_pos: List[int], fuel_cost_func: Callable) -> int:
    return sum(map(partial(fuel_cost_func, aligned_pos=aligned_pos), initial_pos))


def find_minimal_cost_pos(initial_pos: List[int], fuel_cost_func: Callable) -> Tuple[int, int]:
    aligned_pos = range(min(initial_pos), max(initial_pos) + 1)
    costs = list(map(partial(total_fuel_cost, initial_pos=initial_pos, fuel_cost_func=fuel_cost_func), aligned_pos))
    minimum = min(costs)
    index = costs.index(minimum)

    return minimum, index


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().strip().split(',')
    data = [int(d) for d in data]

    # Part 1
    minimum, index = find_minimal_cost_pos(data, fuel_cost)
    print(f'The aligned position minimizing fuel is {index} with {minimum=}.')

    # Part 2
    minimum, index = find_minimal_cost_pos(data, fuel_cost_part2)
    print(f'The aligned position minimizing fuel is {index} with {minimum=}.')
