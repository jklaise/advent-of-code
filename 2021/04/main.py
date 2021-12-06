from itertools import islice
from typing import Iterable, List, Sequence, Tuple, Union

from toolz.curried import map as mapc
from toolz.functoolz import compose, curry


def iterfile(path: str) -> Iterable[str]:
    """
    Utility function to lazily read lines of a file.
    """
    with open(path, 'r') as f:
        yield from f


class Board:

    def __init__(self, board: List[List[Union[int, str]]]) -> None:
        self.board = board
        self.row_marks = [0 for _ in range(5)]
        self.col_marks = [0 for _ in range(5)]

    @curry
    def mark(self, number: int) -> 'Board':
        index_in_row = maybe_index(value=number)
        row_indices = list(map(index_in_row, self.board))
        board_indices = next(((i, j) for (i, j) in enumerate(row_indices) if j is not None), None)
        if board_indices is not None:
            i, j = board_indices
            self.board[i][j] = 'x'
            self.row_marks[i] += 1
            self.col_marks[j] += 1

        return self  # hack to make map work

    def has_won(self) -> bool:
        return self.has_full_row() or self.has_full_col()

    def has_full_row(self) -> bool:
        return 5 in self.row_marks

    def has_full_col(self) -> bool:
        return 5 in self.col_marks


def parse_data(data: Iterable[str]) -> Tuple[List[int], List[Board]]:
    draws = list(map(int, next(data).strip().split(',')))
    boards = []
    while True:
        board = list(islice(data, 6))
        if not board:
            break
        boards.append(parse_board(board))

    return draws, boards


def parse_board(board: List[str]) -> Board:
    board.pop(0)  # remove leading \n
    parse_row = compose(list, mapc(int), str.split, str.strip)  # TODO: figure out how currying works here
    board = list(map(parse_row, board))

    return Board(board)


def find_winning_board(draws: List[int], boards: List[Board]) -> Tuple[int, int]:
    has_won = None
    while not has_won:
        number = draws.pop(0)
        boards = list(map(Board.mark(number=number), boards))
        have_won = list(map(Board.has_won, boards))
        has_won = maybe_index(have_won, True)

    return has_won, number


def find_last_winning_board(draws: List[int], boards: List[Board]) -> Tuple[int, int]:
    n_boards = len(boards)
    n_won = 0
    boards_won_index = []
    while n_won != n_boards:
        number = draws.pop(0)
        boards = list(map(Board.mark(number=number), boards))
        have_won = list(map(Board.has_won, boards))
        indices = [i for i, hw in enumerate(have_won) if hw]
        new_indices = list(set(indices) - set(boards_won_index))
        boards_won_index.extend(new_indices)
        n_won += len(new_indices)
    last_won = boards_won_index[-1]

    return last_won, number


def calculate_score(board: Board, winning_number: int) -> int:
    # TODO: make functional
    summand = 0
    for row in board.board:
        for number in row:
            if isinstance(number, int):
                summand += number
    return summand * winning_number


@curry
def maybe_index(sequence: Sequence, value: int) -> Union[int, None]:
    """
    Return the index of a value in a sequence or None if the value doesn't exist.
    """
    try:
        return sequence.index(value)
    except ValueError:
        return None


if __name__ == '__main__':
    data = iterfile('input.txt')
    draws, boards = parse_data(data)

    # Part 1
    winning_board, winning_number = find_winning_board(draws, boards)
    score = calculate_score(boards[winning_board], winning_number)
    print(f'Score for Part 1 is {score}')

    # Part 2
    data = iterfile('input.txt')
    draws, boards = parse_data(data)

    last_winning_board, last_winning_number = find_last_winning_board(draws, boards)
    score = calculate_score(boards[last_winning_board], last_winning_number)
    print(f'Score for Part 2 is {score}')
