from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
import string


# Part 1 functions
@dataclass
class Instruction:
    num: int
    start: int
    stop: int


def parse_instruction(instruction: str) -> Instruction:
    _, num, _, start, _, stop = instruction.split()
    return Instruction(int(num), int(start), int(stop))


StackColumn = list[str]
Stack = list[StackColumn]


def execute_instruction(stack: Stack, instruction: Instruction) -> Stack:
    start = stack[instruction.start - 1]  # 1 numbering
    stop = stack[instruction.stop - 1]
    assert len(start) >= instruction.num, "Not enough boxes available to move"
    for _ in range(instruction.num):
        crate = start.pop()
        stop.append(crate)
    return stack


def get_top_crates(stack: Stack) -> str:
    return "".join(map(itemgetter(-1), stack))


def parse_stack(input: list[str]) -> Stack:
    height = len(input[:-1])
    n_cols = len(input[-1])
    n_stacks = int(input[-1][-2])  # from the index row
    stack = [[] for _ in range(n_stacks)]
    col_idx = 0
    stack_idx = -1  # indexer for the actual parsed columns
    while col_idx < n_cols:
        # advance across columns to find letters
        while col_idx < n_cols and input[-2][col_idx] not in string.ascii_uppercase:
            col_idx += 1
        # found a stack, now parse it
        stack_idx += 1
        if stack_idx == n_stacks:
            break  # already parsed the last one
        for row_idx in range(height - 1, -1, -1):
            letter = input[row_idx][col_idx]
            if letter not in string.ascii_uppercase:  # reached end of column
                break
            stack[stack_idx].append(letter)
        col_idx += 1
    return stack


def parse_input(input: list[str]) -> tuple[Stack, list[Instruction]]:
    empty_row_idx = input.index("")
    stack = input[:empty_row_idx]  # include index row
    instructions = input[empty_row_idx + 1:]  # ignore empty row
    stack = parse_stack(stack)
    instructions = list(map(parse_instruction, instructions))
    return stack, instructions


# Part 2 functions
def execute_instruction2(stack: Stack, instruction: Instruction) -> Stack:
    start = stack[instruction.start - 1]
    stop = stack[instruction.stop - 1]
    assert len(start) >= instruction.num, "Not enough boxes available to move"
    movable = start[-instruction.num:]
    if not isinstance(movable, list):  # only 1 crate to move
        movable = [movable]
    remainder = start[:-instruction.num]
    stack[instruction.start - 1] = remainder
    stack[instruction.stop - 1] = stop + movable
    return stack


if __name__ == "__main__":
    with open("input.txt") as f:
        # do not use str.strip as it will remove not just \n but all space characters
        # screwing up the numbers on each row!
        input = list(map(lambda x: x.strip('\n'), f.readlines()))
    stack, instructions = parse_input(input)

    # Part 1
    final_stack = reduce(execute_instruction, instructions, stack)
    print(get_top_crates(final_stack))

    # Part 2
    stack, _ = parse_input(input)  # stack has been modified...
    final_stack = reduce(execute_instruction2, instructions, stack)
    print(get_top_crates(stack))
