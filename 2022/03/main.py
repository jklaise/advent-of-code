import string

PRIORITIES: dict[str, int] = {}
for i, letter in enumerate(string.ascii_letters):
    PRIORITIES[letter] = i + 1


# Part 1 functions
def get_compartments(rucksack: str) -> tuple[str, str]:
    n_items = len(rucksack)
    assert n_items % 2 == 0
    first = rucksack[:n_items // 2]
    second = rucksack[n_items // 2:]
    return first, second


def get_priority(item: str) -> int:
    return PRIORITIES[item]


def find_common(first: str, second: str) -> str:
    common = set.intersection(set(first), set(second))
    assert len(common) == 1, f"length is {len(common)}"
    return next(iter(common))


# Part 2 function
def get_groups(rucksacks: list[str]) -> list[list[str]]:
    return [rucksacks[i:i + 3] for i in range(0, len(rucksacks), 3)]


def find_common2(group: list[str]) -> str:
    sets = [set(rucksack) for rucksack in group]
    common = set.intersection(*sets)
    assert len(common) == 1
    return next(iter(common))


if __name__ == "__main__":
    with open("input.txt") as f:
        rucksacks = list(map(str.strip, f.readlines()))

    # Part 1
    sum_priorities = 0
    for ruck in rucksacks:
        first, second = get_compartments(ruck)
        common = find_common(first, second)
        sum_priorities += get_priority(common)
    print(sum_priorities)

    # Part 2
    sum_priorities = 0
    groups = get_groups(rucksacks)
    for group in groups:
        common = find_common2(group)
        sum_priorities += get_priority(common)
    print(sum_priorities)
