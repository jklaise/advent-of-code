from dataclasses import dataclass
from typing import Literal


@dataclass
class Rotation:
    direction: Literal["L", "R"]
    distance: int


@dataclass
class Dial:
    position: int = 50

    def rotate(self, rotation: Rotation) -> int:
        # handle case where we start at 0 and go left - NOT going through zero
        offset = 0
        if self.position == 0 and rotation.direction == "L":
            offset -= 1

        if rotation.direction == "L":
            self.position -= rotation.distance

        elif rotation.direction == "R":
            self.position += rotation.distance

        n_zero = abs(self.position // 100)
        self.position = self.position % 100

        # we already counted the R-rotations ending on xx0
        if self.position == 0 and rotation.direction == "L":
            n_zero += 1

        n_zero += offset
        return n_zero


def parse_rotations(rotations: list[str]) -> list[Rotation]:
    return [Rotation(direction=rot[0], distance=int(rot[1:])) for rot in rotations]


if __name__ == "__main__":
    with open("input.txt") as f:
        rotations = f.read().splitlines()

    rotations = parse_rotations(rotations)

    # Part 1
    counter = 0
    dial = Dial()
    for rotation in rotations:
        _ = dial.rotate(rotation)
        if dial.position == 0:
            counter += 1
    print(counter)

    # Part 2
    counter = 0
    dial = Dial()
    for rotation in rotations:
        n_zero = dial.rotate(rotation)
        counter += n_zero
    print(counter)
