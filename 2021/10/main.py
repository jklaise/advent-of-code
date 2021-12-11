from collections import deque
from enum import Enum
from functools import reduce
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

completion_scores = {
    Char.RIGHT_ROUND: 1,
    Char.RIGHT_SQUARE: 2,
    Char.RIGHT_BRACE: 3,
    Char.RIGHT_ANGLE: 4
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


def find_illegal_char(line: Line) -> Line:
    stack, illegals = Stack(), []
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


#### Part 2 functions
def filter_corrupt(data: List[Line]) -> List[Line]:
    illegal_chars = find_illegal_chars(data)
    return [line for ix, line in enumerate(data) if not illegal_chars[ix]]


def get_completion(line: Line) -> List[Char]:
    stack, illegals = Stack(), []
    stack, _ = reduce(update_stack, line, (stack, illegals))
    completions = []
    while stack:
        item = stack.pop()
        _, name = item.name.split('_')
        completion_name = 'RIGHT_' + name
        completions.append(getattr(Char, completion_name))
    return completions


def score_completion(completion: List[Char]) -> int:
    scores = map(completion_scores.get, completion)
    return reduce(lambda accum, score: 5 * accum + score, scores, 0)


def get_middle_score(scores: List[int]) -> int:
    scores = sorted(scores)
    n = len(scores)
    return scores[int((n - 1) / 2)]


def part2(data: List[Line]) -> int:
    valid = filter_corrupt(data)
    completions = map(get_completion, valid)
    scores = map(score_completion, completions)
    return get_middle_score(scores)


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = parse_data(data)

    # Part 1
    print(f'The answer to part 1 is {part1(data)}')

    # Part 2
    print(f'The answer to part 2 is {part2(data)}')
