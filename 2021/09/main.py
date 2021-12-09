from functools import partial
from itertools import product
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


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    # Part 1
    data = parse_data(data)
    data = pad_data(data)
    print(f'Answer to part 1 is {part1(data)}')
