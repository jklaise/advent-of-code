import math
from collections import Counter
from copy import deepcopy
from itertools import chain, product
from typing import Callable, List, Tuple

Board = List[List[int]]
Coords = Tuple[int, int]

test_data = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def parse_data(data: List[str]) -> Board:
    def parse_line(line: str) -> List[int]:
        return [int(char) for char in line]

    return list(map(parse_line, data))


def pad_data(board: Board) -> Board:
    """Pad the array with a large negative number on the sides"""
    padding = -math.inf
    board = list(map(lambda x: [padding] + x + [padding], board))
    line_length = len(board[0])
    board = [[padding] * line_length] + board + [[padding] * line_length]
    return board


def get_neighbour_coords(coords: Coords) -> List[Coords]:
    x, y = coords
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),
            (x + 1, y + 1)]


def get_max_coords(board: Board) -> Coords:
    xmax = len(board) - 1
    ymax = len(board[0]) - 1
    return xmax, ymax


def get_all_coords(board: Board) -> List[Coords]:
    xmax, ymax = get_max_coords(board)
    coords = list(product(range(1, xmax), range(1, ymax)))
    return coords


def get_value(coords: Coords, board: Board) -> int:
    return board[coords[0]][coords[1]]


def add1(x: int) -> int:
    return x + 1


def update_board(value: int, coords: Coords, board: Board) -> Board:
    new_board = deepcopy(board)  # eurgh
    new_board[coords[0]][coords[1]] = value
    return new_board


def get_to_flash(coords: List[Coords], board: Board) -> List[Coords]:
    to_flash = list(filter(lambda x: get_value(x, board) > 9, coords))
    return to_flash


def flash(to_flash: List[Coords], board: Board, all_flashed: List[Coords]) -> Tuple[Board, List[Coords]]:
    all_flashed.extend(to_flash)
    for coords in to_flash:
        board = update_board(value=0, coords=coords, board=board)
    neighbours = list(chain(*map(get_neighbour_coords, to_flash)))  # non-unique
    neighbours = Counter(neighbours)  # count number of times each neighbour appears
    for neighbour, multiplicity in neighbours.items():
        board = update_board(value=get_value(neighbour, board) + multiplicity, coords=neighbour, board=board)
    to_flash = get_to_flash(list(neighbours.keys()), board)
    if not to_flash:
        for coord in all_flashed:
            board = update_board(0, coord, board)
        return board, all_flashed
    else:
        return flash(to_flash, board, all_flashed)


# TODO: is there a toolz equivalent?
def repeated(func: Callable, n: int) -> Callable:
    if n == 1:
        return func
    return lambda x: func(repeated(func, n - 1)(x))


# TODO: how to avoid this Tuple pattern?
def step(board_and_flashes: Tuple[Board, int]) -> Tuple[Board, int]:
    board, n_flashes = board_and_flashes
    board = [list(map(add1, l)) for l in board]
    to_flash = get_to_flash(get_all_coords(board), board)
    board, all_flashes = flash(to_flash=to_flash, board=board, all_flashed=[])
    return board, n_flashes + len(all_flashes)


# TODO: how to make this functional?
def run_until_synch(board: Board) -> int:
    n_flashes = 0
    n_all = len(get_all_coords(board))
    n_steps = 0
    while n_flashes != n_all:
        board, n_flashes = step((board, 0))
        n_steps += 1
    return n_steps


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()
    board = pad_data(parse_data(data))

    # Part 1
    board_and_flashes = (board, 0)
    board, n_flashes = repeated(step, 100)(board_and_flashes)
    print(f'Answer to part 1 is {n_flashes}')

    # Part 2
    board = pad_data(parse_data(data))
    print(f'Answer to part 2 is {run_until_synch(board)}')
