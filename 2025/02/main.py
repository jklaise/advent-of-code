import textwrap
from dataclasses import dataclass


@dataclass
class IDRange:
    start: int
    end: int

    def gen_ids(self):
        for id in range(self.start, self.end + 1):
            yield id


def parse_range(rng: str) -> IDRange:
    start, end = rng.split("-")
    return IDRange(int(start), int(end))


def is_valid_id_part1(id: int) -> bool:
    strid = str(id)
    size = len(strid)
    if size % 2 == 1:
        return True
    head, tail = strid[: size // 2], strid[size // 2 :]
    if head != tail:
        return True
    return False


def is_valid_id_part2(id: int) -> bool:
    strid = str(id)
    size = len(strid)
    half = size // 2
    part_sizes = [p for p in range(1, half + 1) if size % p == 0]

    for p_size in part_sizes:
        partition = partition_of_size(strid, p_size)
        if all(part == partition[0] for part in partition):
            return False
    return True


def partition_of_size(word: str, n: int) -> list[str]:
    return textwrap.wrap(word, n)


if __name__ == "__main__":
    with open("input.txt") as f:
        ranges = f.read().strip().split(",")
    ranges = [parse_range(r) for r in ranges]

    # Part 1
    id_sum = 0
    for rng in ranges:
        for id in rng.gen_ids():
            if not is_valid_id_part1(id):
                id_sum += id
    print(id_sum)

    # Part 2
    id_sum = 0
    for rng in ranges:
        for id in rng.gen_ids():
            if not is_valid_id_part2(id):
                id_sum += id
    print(id_sum)
