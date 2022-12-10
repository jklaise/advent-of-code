from functools import partial

Grid = list[list[int]]
TreeLine = list[int]
Visibility = list[list[bool]]


def parse_line(line: str) -> list[int]:
    return list(map(int, list(line.strip())))


# Part 1 functions
def transpose(grid: Grid) -> Grid:
    transposed = [[row[i] for row in grid] for i in range(len(grid[0]))]
    return transposed


def are_visible(line: TreeLine) -> list[bool]:
    """
    Check if each tree in a treeline is visible from left to right.
    """
    visibility = [False for _ in range(len(line))]
    max_height = -1
    for i, height in enumerate(line):
        if height > max_height:
            visibility[i] = True
        max_height = max(max_height, height)
    return visibility


def left_visible(line: TreeLine) -> list[bool]:
    return are_visible(line)


def right_visible(line: TreeLine) -> list[bool]:
    return are_visible(line[::-1])[::-1]


def list_or(a: list[bool], b: list[bool]) -> list[bool]:
    return [x | y for x, y in zip(a, b)]


def list_and(a: list[bool], b: list[bool]) -> list[bool]:
    return [x & y for x, y in zip(a, b)]


def row_visible(line: TreeLine) -> list[bool]:
    left = left_visible(line)
    right = right_visible(line)
    return list_or(left, right)


def combine_visibility(row_vis: Visibility, col_vis: Visibility):
    return list(map(list_or, row_vis, col_vis))


def get_visibility(grid: Grid) -> Visibility:
    row_vis = list(map(row_visible, grid))
    col_vis = transpose(list(map(row_visible, transpose(grid))))
    return combine_visibility(row_vis, col_vis)


def count_visible(vis: Visibility) -> int:
    return sum(map(sum, vis))


# Part 2 functions
def scenic_distance(line: TreeLine, index: int) -> int:
    """
    Calculate the scenic score (distance) of one tree in one direction only,
    to the left.
    """
    if index == 0:
        return 0

    score = 0
    height = line[index]
    for ind in range(index - 1, -1, -1):
        score += 1
        if line[ind] >= height:
            break
    return score


def view_left(line: TreeLine) -> list[int]:
    f = partial(scenic_distance, line)
    return list(map(f, range(len(line))))


def view_right(line: TreeLine) -> list[int]:
    f = partial(scenic_distance, line[::-1])
    return list(map(f, range(len(line))))[::-1]


def list_mul(a: list[int], b: list[int]) -> list[int]:
    return [x * y for x, y in zip(a, b)]


def row_scenic(line: TreeLine) -> list[int]:
    sl = view_left(line)
    sr = view_right(line)
    return list_mul(sl, sr)


def combine_scores(row_scores: list[list[int]], col_scores: list[list[int]]) -> list[list[int]]:
    return list(map(list_mul, row_scores, col_scores))


def get_scenic_scores(grid: Grid) -> list[list[int]]:
    row_scores = list(map(row_scenic, grid))
    col_scores = transpose(list(map(row_scenic, transpose(grid))))
    return combine_scores(row_scores, col_scores)


if __name__ == "__main__":
    with open("input.txt") as f:
        grid = list(map(parse_line, f.readlines()))

    # Part 1 - would be easier with numpy...
    vis = get_visibility(grid)
    print(count_visible(vis))

    # Part 2
    scenic_scores = get_scenic_scores(grid)
    print(max(map(max, scenic_scores)))
