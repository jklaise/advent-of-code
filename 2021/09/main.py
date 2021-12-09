from dataclasses import dataclass
from typing import List, Sequence

Map = List[List[int]]


@dataclass
class Point:
    x: int
    y: int
    value: int


def parse_line(line: str) -> List[int]:
    return [int(n) for n in line]


def parse_data(data: List[str]) -> List[List[int]]:
    return list(map(parse_line, data))


def maybe_get(index: int, sequence: Sequence):
    try:
        return sequence[index]
    except IndexError:
        return None


def is_low_point(point: int, heightmap: Map) -> bool:


def find_low_points() -> List[int]


def risk_level(low_point: int) -> int:
    return low_point + 1


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = parse_data(data)
