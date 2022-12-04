from dataclasses import dataclass


# Part 1 functions
@dataclass
class Range:
    min: int
    max: int


Pair = tuple[Range, Range]


def parse_range(range: str) -> Range:
    min, max = map(int, range.split('-'))
    return Range(min, max)


def parse_pair(pair: str) -> Pair:
    ranges = pair.split(',')
    first, second = map(parse_range, ranges)
    return first, second


def first_subrange_of_second(pair: Pair) -> bool:
    first, second = pair
    return first.min >= second.min and first.max <= second.max


def fully_contained(pair: Pair) -> bool:
    first, second = pair
    return first_subrange_of_second(pair) or first_subrange_of_second((second, first))


# Part 2 functions
def first_overlaps_second(pair: Pair) -> bool:
    first, second = pair
    return second.min >= first.min and second.min <= first.max


def overlapping(pair: Pair) -> bool:
    first, second = pair
    return first_overlaps_second(pair) or first_overlaps_second((second, first))


if __name__ == "__main__":
    with open("input.txt") as f:
        parser_fn = lambda line: parse_pair(str.strip(line))
        pairs = list(map(parser_fn, f.readlines()))

    # Part 1
    num_fully_contained = sum(map(fully_contained, pairs))
    print(num_fully_contained)

    # Part 2
    num_overlaps = sum(map(overlapping, pairs))
    print(num_overlaps)
