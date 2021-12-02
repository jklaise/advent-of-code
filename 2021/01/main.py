from itertools import tee
from operator import gt

if __name__ == '__main__':
    with open('input.txt') as f:
        readings = list(map(int, f.readlines()))

    # Part 1
    n_increases = sum(map(gt, readings[1:], readings))
    print(n_increases)

    # Part 2
    sums = map(sum, zip(readings, readings[1:], readings[2:]))

    # is there a better way than using tee and advancing one of the iterables?
    sums, sums_1 = tee(sums, 2)
    next(sums_1)

    n_increases = sum(map(gt, sums_1, sums))
    print(n_increases)
