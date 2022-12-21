from dataclasses import dataclass
from functools import cmp_to_key

Packet = list[int | list]  # needs a recursive definition


@dataclass
class Pair:
    left: Packet
    right: Packet


def parse_pair(pair: str) -> Pair:
    left, right = pair.split("\n")
    return Pair(eval(left), eval(right))


def parse_packets(packets: str) -> list[Pair]:
    pairs = packets.split("\n\n")
    return list(map(parse_pair, pairs))


def compare(pair: Pair) -> bool:
    # could be done much better with fewer chances for bugs...
    left, right = pair.left, pair.right
    lenl, lenr = len(left), len(right)
    for i in range(min(lenl, lenr)):
        l, r = left[i], right[i]
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            elif l > r:
                return False
        else:
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            result = compare(Pair(l, r))
            if result is not None:
                return result
            else:
                continue

    if lenl < lenr:
        return True
    elif lenl > lenr:
        return False


# Part 2 functions
def cmp(a: Packet, b: Packet) -> int:
    """
    Old-style comparison function for use with functools.cmp_to_key:
    https://docs.python.org/3/library/functools.html#functools.cmp_to_key
    """
    value = compare(Pair(a, b))
    if value:
        return -1
    return 1


if __name__ == "__main__":
    with open("input.txt") as f:
        packets = f.read().strip()

    pairs = parse_packets(packets)

    # Part 1
    correct = list(map(compare, pairs))
    print(sum([i + 1 for i, x in enumerate(correct) if x]))  # 1-indexing

    # Part 2
    packets = [eval(p) for p in packets.split("\n") if p != '']
    packets.extend([[[2]], [[6]]])

    out = sorted(packets, key=cmp_to_key(cmp))
    div_ix_1 = out.index([[2]]) + 1
    div_ix_2 = out.index([[6]]) + 1
    print(div_ix_1 * div_ix_2)
