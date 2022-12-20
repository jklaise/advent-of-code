import string
from copy import deepcopy
from dataclasses import dataclass
from functools import partial

# Part 1 functions
Map = list[list[str]]


@dataclass(frozen=True)
class Coord:
    row: int
    col: int


Path = list[Coord]


def coord2char(coord: Coord, heights: Map) -> str:
    return heights[coord.row][coord.col]


def can_go(source: str, target: str) -> bool:
    diff = ord(target) - ord(source)
    if diff <= 1:
        return True
    return False


def get_neighbours(source: Coord) -> tuple[Coord, ...]:
    up = Coord(source.row - 1, source.col)
    down = Coord(source.row + 1, source.col)
    left = Coord(source.row, source.col - 1)
    right = Coord(source.row, source.col + 1)
    return up, down, left, right


NEIGHBOURS_CACHE: dict[Coord, list[Coord]] = {}


# this function is memoized to avoid computing the same neighbours
# for many different paths
def viable_neighbours(source: Coord, heights: Map) -> list[Coord]:
    if source in NEIGHBOURS_CACHE:
        return NEIGHBOURS_CACHE[source]
    source_char = coord2char(source, heights)
    neighbours = get_neighbours(source)
    viable = []
    for nb in neighbours:
        target_char = coord2char(nb, heights)
        if can_go(source_char, target_char):
            viable.append(nb)
    NEIGHBOURS_CACHE[source] = viable
    return viable


def expand_path(path: Path, continuations: set[Coord]) -> list[Path]:
    new_paths = []
    for cont in continuations:
        # skip paths whose continuation is already in the shortest cache
        # note: this also takes care of any backtracking paths
        if cont in SHORTEST_PATH_ENDING_AT_COORD:
            continue
        new = deepcopy(path)
        new.append(cont)
        new_paths.append(new)
    return new_paths


def unique_path_ends(paths: list[Path]) -> set[Coord]:
    return set(path[-1] for path in paths)


def shortest_so_far_with_unique_ends(paths: list[Path], unique_ends: set[Coord]) -> list[Path]:
    shortest = []
    # unique_ends = unique_path_ends(paths)
    for end in unique_ends:
        ending_with = sorted(filter(lambda x: x[-1] == end, paths), key=len)
        shortest.append(ending_with[0])
    return shortest


SHORTEST_PATH_ENDING_AT_COORD: dict[Coord, Path] = {}


def is_end(heights: Map, end: Coord | str, cand: Coord) -> bool:
    if isinstance(end, Coord):
        return cand == end
    return coord2char(cand, heights) == end


def find_paths(heights: Map, end: Coord | str, paths: list[Path]) -> set[Coord]:
    for path in paths:
        SHORTEST_PATH_ENDING_AT_COORD[path[-1]] = path
    # we only need to consider possible continuations for the set of unique new
    # squares (current path ends) visited
    unique_ends = unique_path_ends(paths)
    finished = any(map(partial(is_end, heights, end), unique_ends))
    if finished:
        return unique_ends
    # furthermore, we only need to consider one path, the shortest one, ending on
    # a certain square
    paths = shortest_so_far_with_unique_ends(paths, unique_ends)
    new_paths = []
    continuations = {end: viable_neighbours(end, heights) for end in unique_ends}
    for path in paths:
        new_paths.extend(expand_path(path, continuations[path[-1]]))
    # recurse
    return find_paths(heights, end, new_paths)


def parse_map(heights: str) -> tuple[Map, Coord, Coord]:
    rows = []
    row_ix, col_ix = 0, 0
    current_row = []
    for char in heights:
        if char == "S":
            start = Coord(row_ix + 1, col_ix + 1)  # padding
            char = "a"
        elif char == "E":
            end = Coord(row_ix + 1, col_ix + 1)  # padding
            char = "z"
        if char != "\n":
            current_row.append(char)
            col_ix += 1
        else:
            rows.append(current_row)
            current_row = []
            row_ix += 1
            col_ix = 0

    # we pad the sides with `~` (ascii code 126, so inaccessible)
    # to not worry about edge cases separately later
    for row in rows:
        row.insert(0, '~')
        row.append('~')
    length = len(rows[0])
    rows.insert(0, ['~'] * length)
    rows.append(['~'] * length)

    return rows, start, end


# Part 2 functions
def invert_map(heights: Map) -> Map:
    letters = string.ascii_lowercase
    for row in range(len(heights)):
        for col in range(len(heights[0])):
            char = heights[row][col]
            if char != "~":
                index = letters.index(char)
                new_index = len(letters) - index - 1
                new_char = letters[new_index]
                heights[row][col] = new_char
    return heights


def main():
    with open("input.txt") as f:
        heights = f.read()
    heights, start, end = parse_map(heights)

    # Part 1
    # We perform BFS until one path hits the end coordinate. Note that keeping track of all
    # unique paths is infeasible both time and space-wise. But a trick is to only keep track
    # of the shortest path finishing at any coordinate. Because of BFS, by definition the first
    # time we visit a coordinate, we arrive via a shortest path.
    global SHORTEST_PATH_ENDING_AT_COORD
    global NEIGHBOURS_CACHE
    start_paths = [[start]]
    find_paths(heights, end, start_paths)
    print(len(SHORTEST_PATH_ENDING_AT_COORD[end]) - 1)  # number of steps is 1 less length

    # Part 2
    # We "invert" the heights and start from the end coordinate and stop as soon as we hit
    # the first "a" square
    heights = invert_map(heights)
    NEIGHBOURS_CACHE = {}
    SHORTEST_PATH_ENDING_AT_COORD = {}
    start_paths = [[end]]
    unique_ends = find_paths(heights, "z", start_paths)
    for end in unique_ends:
        if coord2char(end, heights) == "z":
            print(len(SHORTEST_PATH_ENDING_AT_COORD[end]) - 1)


if __name__ == "__main__":
    main()
