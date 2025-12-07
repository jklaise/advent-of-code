from dataclasses import dataclass
import textwrap

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]


@dataclass
class Position:
    x: int
    y: int


def check_pos(board: list[list[str]], pos: Position) -> bool | None:
    rows = len(board)
    cols = len(board[0])

    if board[pos.x][pos.y] != "@":
        return

    n_rolls = 0
    for dir in DIRECTIONS:
        new_pos = Position(pos.x + dir[0], pos.y + dir[1])
        if (
            new_pos.x < 0
            or new_pos.y < 0
            or new_pos.x > rows - 1
            or new_pos.y > cols - 1
        ):
            continue

        roll = board[new_pos.x][new_pos.y]
        if roll == "@":
            n_rolls += 1
    if n_rolls < 4:
        return True
    return False


def n_accessible(board: list[list[str]], remove: bool = False) -> int:
    pos_accessible = []
    for x in range(rows):
        for y in range(cols):
            pos = Position(x, y)
            if check_pos(board, pos):
                pos_accessible.append(pos)
    if remove:
        for pos in pos_accessible:
            board[pos.x][pos.y] = "."
    return len(pos_accessible)


if __name__ == "__main__":
    with open("input.txt") as f:
        board = f.read().splitlines()
    board = [textwrap.wrap(line, 1) for line in board]

    rows = len(board)
    cols = len(board[0])

    # Part 1
    print(n_accessible(board))

    # Part 2
    total_removable = 0
    removable = 1
    while removable != 0:
        removable = n_accessible(board, remove=True)
        total_removable += removable
    print(total_removable)
