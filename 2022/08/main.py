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

if __name__ == "__main__":
    with open("input.txt") as f:
        grid = list(map(parse_line, f.readlines()))

    # Part 1 - would be easier with numpy...
    vis = get_visibility(grid)
    print(count_visible(vis))

    # Part 2
