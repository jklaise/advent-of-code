from copy import deepcopy
from functools import partial, reduce
from itertools import chain, product
from operator import mul
from typing import List, Tuple

test_data = ["2199943210",
             "3987894921",
             "9856789892",
             "8767896789",
             "9899965678"]

Map = List[List[int]]
Coords = Tuple[int, int]


def parse_line(line: str) -> List[int]:
    return [int(n) for n in line]


def parse_data(data: List[str]) -> Map:
    return list(map(parse_line, data))


def pad_data(data: Map, padding: int = 100) -> Map:
    """Pad the array with a large number on the sides"""
    data = list(map(lambda x: [padding] + x + [padding], data))
    line_length = len(data[0])
    data = [[padding] * line_length] + data + [[padding] * line_length]
    return data


def get_max_coords(data: Map) -> Coords:
    x_max = len(data) - 1
    y_max = len(data[0]) - 1
    return x_max, y_max


def get_neighbour_coords(coords: Coords) -> List[Coords]:
    x, y = coords
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def get_height_from_coords(coords: Coords, data: Map) -> int:
    return data[coords[0]][coords[1]]


def is_low_point(coords: Coords, data: Map) -> bool:
    coords_height = get_height_from_coords(coords, data)
    neighbours = get_neighbour_coords(coords)
    neigbour_heights = list(map(partial(get_height_from_coords, data=data), neighbours))
    if coords_height < min(neigbour_heights):
        return True
    else:
        return False


def find_low_points(data: Map) -> List[Coords]:
    x_max, y_max = get_max_coords(data)
    # TODO: for some reason doesnt work without conversion to list (yuge)
    coords = list(product(range(1, x_max), range(1, y_max)))
    are_low_points = list(map(partial(is_low_point, data=data), coords))
    return [coord for coord, is_low in zip(coords, are_low_points) if is_low]


def get_risk(height: int) -> int:
    return height + 1


def part1(data: Map) -> int:
    coords_low = find_low_points(data)
    heights = list(map(partial(get_height_from_coords, data=data), coords_low))
    risks = list(map(get_risk, heights))
    return sum(risks)


####### Part 2 functions
def set_height_from_coords(value: int, coords: Coords, data: Map) -> Map:
    new_data = deepcopy(data)  # eurgh
    new_data[coords[0]][coords[1]] = value
    return new_data


def find_higher_neighbours(coords: Coords, data: Map) -> List[Coords]:
    neighbours = get_neighbour_coords(coords)
    return discard_peaks(neighbours, data)


def find_basin(coords: Coords, data: Map, basin: List) -> List[Coords]:
    # if we start, then add initial point to the basin (otherwise off by one)
    if not basin:
        basin = [coords]
    data = set_height_from_coords(9, coords, data)  # not mutating...
    neighbours = find_higher_neighbours(coords, data)
    basin = basin + neighbours
    if not neighbours:
        return basin
    else:
        # Here we recurse, however we map the recursion across all neighbours.
        # Since we map it, we need to use `chain` to extract the sublists and get a flattened list.
        # Since we map it, we also need to remove duplicates (using set) - note memory consumption isn't good
        return list(set(chain(*map(partial(find_basin, data=data, basin=basin), neighbours))))  # ewww


def discard_peaks(coords: List[Coords], data: Map, padding: int = 100) -> List[Coords]:
    "Don't consider points of height 9 and boundaries as part of a basin."
    heights = list(map(partial(get_height_from_coords, data=data), coords))
    return [coord for coord, height in zip(coords, heights) if height not in [9, padding]]


def find_basins(data: Map) -> List[List[Coords]]:
    low_points = find_low_points(data)
    initial_basins = [[] for _ in low_points]
    all_basins = [find_basin(lp, data, ib) for lp, ib in zip(low_points, initial_basins)]
    return all_basins


def part2(data: Map) -> int:
    all_basins = find_basins(data)
    top_three = sorted(all_basins, key=len, reverse=True)[:3]
    return reduce(mul, map(len, top_three))


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    # Part 1
    data = parse_data(data)
    data = pad_data(data)
    print(f'Answer to part 1 is {part1(data)}')

    # Part 2
    print(f'Answer to part 2 is {part2(data)}')
