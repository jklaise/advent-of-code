from collections import deque
from enum import Enum
from functools import reduce
from operator import itemgetter
from typing import List, Optional, Tuple


class Char(str, Enum):
    LEFT_ROUND = '('
    RIGHT_ROUND = ')'
    LEFT_SQUARE = '['
    RIGHT_SQUARE = ']'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_ANGLE = '<'
    RIGHT_ANGLE = '>'


scores = {
    Char.RIGHT_ROUND: 3,
    Char.RIGHT_SQUARE: 57,
    Char.RIGHT_BRACE: 1197,
    Char.RIGHT_ANGLE: 25137
}

test_data = ["[({(<(())[]>[[{[]{<()<>>",
             "[(()[<>])]({[<{<<[]>>(",
             "{([(<{}[<>[]}>{[]{[(<()>",
             "(((({<>}<{<{<>}{[]{[]{}",
             "[[<[([]))<([[{}[[()]]]",
             "[{[{({}]{}}([{[{{{}}([]",
             "{<[[]]>}<{[{[{[]{()[[[]",
             "[<(<(<(<{}))><([]([]()",
             "<{([([[(<>()){}]>(<<{{",
             "<{([{{}}[<[[[<>{}]]]>[]]", ]

Line = List[Char]
Stack = deque[Char]


def parse_line(line: str) -> Line:
    return list(map(lambda x: Char(x), line))


def parse_data(data: List[str]) -> List[Line]:
    return list(map(parse_line, data))


def is_matching(prev: Char, next: Char) -> bool:
    orientation1, type1 = prev.name.split('_')
    orientation2, type2 = next.name.split('_')
    return [orientation1, orientation2] == ['LEFT', 'RIGHT'] and type1 == type2


def is_illegal(prev: Char, next: Char) -> bool:
    orientation1, type1 = prev.name.split('_')
    orientation2, type2 = next.name.split('_')
    return [orientation1, orientation2] == ['LEFT', 'RIGHT'] and type1 != type2


def update_stack(stack_and_illegals: Tuple[Stack, Line], char: Char) -> Tuple[Stack, Line]:
    stack, illegals = stack_and_illegals
    # empty stack:
    if not stack:
        stack.append(char)
    else:
        prev = stack[-1]
        if is_matching(prev, char):
            stack.pop()
        elif is_illegal(prev, char):
            illegals.append(char)
            stack.append(char)
        else:
            stack.append(char)
    return stack, illegals


def find_illegal_char(line: Line) -> Optional[Line]:
    stack = Stack()
    illegals = []
    stack, illegals = reduce(update_stack, line, (stack, illegals))
    return illegals


def find_illegal_chars(data: List[Line]) -> List[Line]:
    chars = map(find_illegal_char, data)
    return list(chars)


def part1(data: List[Line]) -> int:
    illegal_chars = find_illegal_chars(data)
    illegal_chars = filter(lambda x: x, illegal_chars)  # remove []
    illegal_chars = [char[0] for char in illegal_chars]  # select only element
    return sum(map(scores.get, illegal_chars))


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = parse_data(data)

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')
