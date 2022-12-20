from copy import deepcopy
from dataclasses import dataclass
from functools import cache, partial

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


def is_backtrack(path: Path) -> bool:
    return len(path) != len(set(path))


def is_finished(path: Path, end: Coord) -> bool:
    return path[-1] == end


def viable_paths(heights: Map, path: Path) -> list[Path]:
    viable = []
    nbs = viable_neighbours(path[-1], heights)
    for nb in nbs:
        new_path = deepcopy(path)
        new_path.append(nb)
        viable.append(new_path)

    return viable


def expand_path(path: Path, continuations: set[Coord]) -> list[Path]:
    new_paths = []
    for cont in continuations:
        # skip paths that would backtrack
        if cont in path:
            # print("skipping")
            continue
        # skip paths whose continuation is already in the shortest cache
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


def find_paths(heights: Map, end: Coord, paths: list[Path]) -> list[Path]:
    print(f"#paths: {len(paths)}")
    for path in paths:
        SHORTEST_PATH_ENDING_AT_COORD[path[-1]] = path
    # finished = any((is_finished(path, end) for path in paths))
    # filter any bactracking paths as won't be shortest
    paths = list(filter(lambda x: not is_backtrack(x), paths))
    print(f"#paths after filtering: {len(paths)}")
    # we only need to keep one path, the shortest so far, ending on a certain square
    unique_ends = unique_path_ends(paths)
    finished = any(map(lambda x: x == end, unique_ends))
    if finished:
        return paths
    paths = shortest_so_far_with_unique_ends(paths, unique_ends)
    print(f"#paths after filtering: {len(paths)}\n")
    new_paths = []
    # unique_ends = unique_path_ends(paths)
    continuations = {end: viable_neighbours(end, heights) for end in unique_ends}
    for path in paths:
        # new_paths.extend(viable_paths(heights, path))
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


def main():
    with open("input.txt") as f:
        heights = f.read()
    heights, start, end = parse_map(heights)

    # here we need to memoize the `viable_neighbours` functions as it's called
    # repeatedly with many of the same paths and forms a bottleneck

    # Part 1
    start_paths = [[start]]
    candidate_paths = find_paths(heights, end, start_paths)
    shortest = min(map(len, candidate_paths)) - 1  # number of steps is 1 less length
    print(shortest)


if __name__ == "__main__":
    main()
