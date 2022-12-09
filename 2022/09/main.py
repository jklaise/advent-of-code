from copy import copy
from dataclasses import dataclass
from functools import reduce


@dataclass
class Motion:
    direction: str
    steps: int


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Head:
    pos: Position


@dataclass
class Tail:
    pos: Position
    history: list[Position]


def initialize() -> tuple[Head, Tail]:
    start = (0, 0)
    return Head(Position(*start)), Tail(Position(*start), history=[Position(*start)])


def parse_motion(motion: str) -> Motion:
    direction, steps = motion.strip().split()
    return Motion(direction, int(steps))


def execute_motion(motion: Motion, head: Head, tail: Tail) -> tuple[Head, Tail]:
    for step in range(motion.steps):
        head, tail = execute_step(motion.direction, head, tail)
    return head, tail


def step_up(end: Head | Tail) -> Head | Tail:
    end.pos.y += 1
    return end


def step_down(end: Head | Tail) -> Head | Tail:
    end.pos.y -= 1
    return end


def step_left(end: Head | Tail) -> Head | Tail:
    end.pos.x -= 1
    return end


def step_right(end: Head | Tail) -> Head | Tail:
    end.pos.x += 1
    return end


STEPS = {
    'U': step_up,
    'D': step_down,
    'L': step_left,
    'R': step_right
}


def execute_step(direction: str, head: Head, tail: Tail) -> tuple[Head, Tail]:
    head = step_head(direction, head)
    tail = step_tail(head, tail)
    return head, tail


def step_head(direction: str, head: Head) -> Head:
    return STEPS[direction](head)


def taxicab_distance(head: Head, tail: Tail) -> int:
    x_delta = head.pos.x - tail.pos.x
    y_delta = head.pos.y - tail.pos.y
    return abs(x_delta) + abs(y_delta)


def are_next_to(head: Head, tail: Tail) -> bool:
    return taxicab_distance(head, tail) == 1


def are_diagonal(head: Head, tail: Tail) -> bool:
    taxi = taxicab_distance(head, tail)
    return taxi == 2 and head.pos.x != tail.pos.x and head.pos.y != tail.pos.y


def are_on_top(head: Head, tail: Tail) -> bool:
    return head.pos == tail.pos


def are_same_row(head: Head, tail: Tail) -> bool:
    return head.pos.x == tail.pos.x


def step_diag(head: Head, tail: Tail) -> Tail:
    if tail.pos.y < head.pos.y:
        tail = step_up(tail)
    else:
        tail = step_down(tail)
    if tail.pos.x < head.pos.x:
        tail = step_right(tail)
    else:
        tail = step_left(tail)
    return tail


def are_same_col(head: Head, tail: Tail) -> bool:
    return head.pos.y == tail.pos.y


def step_tail(head: Head, tail: Tail) -> Tail:
    if are_on_top(head, tail) or are_next_to(head, tail) or are_diagonal(head, tail):
        return tail
    elif are_same_row(head, tail):
        assert abs(head.pos.y - tail.pos.y) == 2
        if head.pos.y > tail.pos.y:
            tail = step_up(tail)
        else:
            tail = step_down(tail)
    elif are_same_col(head, tail):
        assert abs(head.pos.x - tail.pos.x) == 2
        if head.pos.x > tail.pos.x:
            tail = step_right(tail)
        else:
            tail = step_left(tail)
    else:  # diagonal step
        assert taxicab_distance(head, tail) == 3
        tail = step_diag(head, tail)
    tail.history.append(copy(tail.pos))
    return tail


if __name__ == "__main__":
    with open("input.txt") as f:
        motions = list(map(parse_motion, f.readlines()))

    # Part 1
    head, tail = initialize()
    for motion in motions:
        head, tail = execute_motion(motion, head, tail)
    print(len(set(tail.history)))
