from dataclasses import dataclass


@dataclass
class Range:
    lo: int
    hi: int


@dataclass
class Database:
    ranges: list[Range]
    ingredients: list[int]

    def sort(self) -> None:
        self.ranges = sorted(self.ranges, key=lambda r: (r.lo, r.hi))
        self.ingredients.sort()


def parse(input: str) -> Database:
    rngs, ings = input.split("\n\n")
    rngs = [rng.strip() for rng in rngs.splitlines()]

    ranges = [Range(int(rng[0]), int(rng[1])) for rng in [r.split("-") for r in rngs]]
    ingredients = [int(ing.strip()) for ing in ings.splitlines()]

    return Database(ranges, ingredients)


def is_fresh(ing: int, rng: Range) -> bool:
    return ing >= rng.lo and ing <= rng.hi


def part1(db: Database) -> int:
    counter = 0
    for ing in db.ingredients:
        for rng in db.ranges:
            if is_fresh(ing, rng):
                counter += 1
                break

    return counter


def expand_range(rng: Range) -> set[int]:
    return set(range(rng.lo, rng.hi + 1))


def part2(db: Database) -> int:
    db.sort()
    n_fresh = 0
    prev = Range(0, 0)

    for rng in db.ranges:
        n_fresh += rng.hi - rng.lo + 1
        if rng.lo <= prev.hi:
            if rng.hi > prev.hi:  # not nested
                n_fresh -= prev.hi - rng.lo + 1
            elif rng.hi <= prev.hi:  # nested
                n_fresh -= rng.hi - rng.lo + 1
        prev = rng

    return n_fresh


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()

        db = parse(input)

        # Part 1
        n_fresh = part1(db)
        print(n_fresh)

        # Part 2
        n_rng_fresh = part2(db)
        print(n_rng_fresh)
