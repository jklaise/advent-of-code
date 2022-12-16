from collections import deque
from dataclasses import dataclass
from functools import reduce
from operator import add, mul
import re

from typing import Callable, Literal


def ints(str) -> list[int]:
    return list(map(int, re.findall('[0-9]+', str)))


@dataclass
class Operation:
    op: Callable[[int, int], int]
    quantity: int | Literal['old']

    def execute(self, old: int) -> int:
        if isinstance(self.quantity, int):
            return self.op(old, self.quantity)
        else:
            return self.op(old, old)


@dataclass
class Test:
    quotient: int
    if_true: int
    if_false: int

    def execute(self, value: int) -> bool:
        return value % self.quotient == 0


@dataclass
class Monkee:
    items: deque[int]
    operation: Operation
    test: Test
    _inspections: int = 0

    @property
    def inspections(self):
        return self._inspections

    def inspect(self, relief: int = None, lcm: int = None) -> tuple[int, int]:
        self._inspections += 1
        worry = self.items.popleft()
        worry = self.operation.execute(worry)
        if relief:
            worry //= relief
        elif lcm:
            # take the remainder of the test
            worry = worry % lcm
        test_outcome = self.test.execute(worry)
        if test_outcome:
            return (worry, self.test.if_true)
        return (worry, self.test.if_false)

    def throw(self, item: int, recipient: int, monkees: 'MonkeeComittee'):
        monkees[recipient].items.append(item)


MonkeeComittee = list[Monkee]


def parse_operation(op: str) -> Operation:
    op_map = {"*": mul, "+": add}
    quantity = ints(op)
    if not quantity:
        quantity = "old"
    else:
        quantity = quantity[0]
    op_str = op.split("=")[-1].strip().split()[1]
    op = op_map[op_str]
    return Operation(op, quantity)


def parse_test(test: list[str]) -> Test:
    quotient = ints(test[0])[0]
    if_true = ints(test[1])[0]
    if_false = ints(test[2])[0]
    return Test(quotient, if_true, if_false)


def parse_monkee(monkee: list[str]) -> Monkee:
    items = deque(ints(monkee[1]))
    operation = parse_operation(monkee[2])
    test = parse_test(monkee[3:])
    return Monkee(items, operation, test)


def execute_round(monkees: MonkeeComittee, relief: int = None, lcm: int = None):
    for monkee in monkees:
        while monkee.items:
            worry, recipient = monkee.inspect(relief, lcm)
            monkee.throw(worry, recipient, monkees)


def monkey_business(monkees: MonkeeComittee) -> int:
    inspections = sorted([m.inspections for m in monkees], reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    with open("input.txt") as f:
        monkees_str = list(map(lambda x: x.split("\n"), f.read().split("\n\n")))

    # Part 1
    monkees = list(map(parse_monkee, monkees_str))
    ROUNDS = 20
    for _ in range(ROUNDS):
        execute_round(monkees, relief=3)
    print(monkey_business(monkees))

    # Part 2
    monkees = list(map(parse_monkee, monkees_str))
    ROUNDS = 10000
    # Take the lcm of the individual test quotients, and only keep
    # worry values modulo this lcm
    lcm = reduce(mul, [m.test.quotient for m in monkees])
    for _ in range(ROUNDS):
        execute_round(monkees, lcm=lcm)
    print(monkey_business(monkees))
