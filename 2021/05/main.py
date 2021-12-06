from collections import Counter
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain
from typing import List

test_data = ["0,9 -> 5,9",
             "8,0 -> 0,8",
             "9,4 -> 3,4",
             "2,2 -> 2,1",
             "7,0 -> 7,4",
             "6,4 -> 2,0",
             "0,9 -> 2,9",
             "3,4 -> 1,4",
             "0,0 -> 8,8",
             "5,5 -> 8,2"]


def read_lines(path: str) -> List[str]:
    with open(path) as f:
        lines = f.read().splitlines()
    return lines


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_diagonal(self) -> bool:
        return abs(self.start.x - self.end.x) == abs(self.start.y - self.end.y)


def parse_lines(lines: List[str]) -> List[Line]:
    def point_to_point(point: str) -> Point:
        x, y = list(map(int, point.split(',')))
        return Point(x, y)

    def line_to_line(line: str) -> Line:
        start, end = line.split(' -> ')
        start = point_to_point(start)
        end = point_to_point(end)
        return Line(start, end)

    return list(map(line_to_line, lines))


VentMap = List[List[int]]


def create_vent_map(lines: List[Line]) -> VentMap:
    max_x = lambda line: max(line.start.x, line.end.x)
    max_y = lambda line: max(line.start.y, line.end.y)
    width = reduce(max, map(max_y, lines)) + 1
    height = reduce(max, map(max_x, lines)) + 1
    vent_map = [[0 for col in range(width)] for row in range(height)]
    return vent_map


def update_vent_map(vent_map: VentMap, line: Line, diagonal: bool = False) -> VentMap:
    if line.is_horizontal():
        y = line.start.y
        xs = range(min(line.start.x, line.end.x), max(line.start.x, line.end.x) + 1)
        for x in xs:
            vent_map[y][x] += 1
    elif line.is_vertical():
        x = line.start.x
        ys = range(min(line.start.y, line.end.y), max(line.start.y, line.end.y) + 1)
        for y in ys:
            vent_map[y][x] += 1
    elif line.is_diagonal() and diagonal:
        x_pad = 1 if line.start.x < line.end.x else -1
        y_pad = 1 if line.start.y < line.end.y else -1
        xs = range(line.start.x, line.end.x + x_pad, x_pad)
        ys = range(line.start.y, line.end.y + y_pad, y_pad)
        for x, y in zip(xs, ys):
            vent_map[y][x] += 1
    else:
        raise ValueError(f'{line=} is neither horizontal nor vertical, nor diagonal')
    return vent_map


def count_crossings(vent_map: VentMap, greater_than: int = 1) -> int:
    counts = Counter(chain(*vent_map))
    total = sum([v for k, v in counts.items() if k > greater_than])
    return total


if __name__ == '__main__':
    lines = read_lines('input.txt')
    lines = parse_lines(lines)

    # Part 1
    hor_and_ver_lines = list(filter(lambda x: Line.is_horizontal(x) or Line.is_vertical(x), lines))
    vent_map = create_vent_map(lines)

    final_vent_map = reduce(update_vent_map, hor_and_ver_lines, vent_map)
    crossings = count_crossings(final_vent_map)
    print(f'Answer to part 1: {crossings}')

    # Part 2
    hor_ver_diag_lines = list(filter(lambda x: Line.is_horizontal(x)
                                               or Line.is_vertical(x)
                                               or Line.is_diagonal(x), lines))

    vent_map = create_vent_map(lines)
    final_vent_map = reduce(partial(update_vent_map, diagonal=True), hor_ver_diag_lines, vent_map)
    crossings = count_crossings(vent_map)
    print(f'Answer to part 2: {crossings}')
