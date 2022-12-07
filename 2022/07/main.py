from collections import defaultdict


def is_command(line: str) -> bool:
    return line.startswith('$')


def is_cd(line: str) -> bool:
    return line.startswith('$ cd')


def get_cd_dir(line: str) -> str:
    dir = line.split()[-1]
    return dir


def is_dir(line: str) -> bool:
    return line.startswith('dir')


def get_dir_name(line: str) -> str:
    return line.split()[-1]


def parse_file_ls(line: str) -> tuple[int, str]:
    split = line.split()
    return (int(split[0]), split[1])


def update_cd(cd: tuple[str, ...], dir: str) -> tuple[str, ...]:
    if not cd:
        return (dir,)
    if dir == '..':
        return cd[:-1]
    else:
        return cd + (dir,)


def make_dir_sizes(lines: list[str]) -> dict[tuple, int]:
    dirs = defaultdict(int)
    cd = ()
    for line in lines:
        if is_cd(line):
            dir = get_cd_dir(line)
            cd = update_cd(cd, dir)
        elif not is_command(line):
            if not is_dir(line):
                size, _ = parse_file_ls(line)
                # update all nested dirs at once
                for d_ix in range(len(cd)):
                    dirs[cd[:d_ix + 1]] += size
    return dirs


# Part 2 functions
TOTAL_SPACE = 70_000_000
NEEDED_SPACE = 30_000_000


def size_to_free(dir_sizes: dict[tuple, int]) -> int:
    return NEEDED_SPACE - (TOTAL_SPACE - dir_sizes[('/',)])


if __name__ == "__main__":
    with open('input.txt') as f:
        lines = list(map(str.strip, f.readlines()))

    # Part 1
    dir_sizes = make_dir_sizes(lines)
    print(sum(filter(lambda x: x <= 100_000, dir_sizes.values())))

    # Part2
    to_free = size_to_free(dir_sizes)
    print(min(filter(lambda x: x >= to_free, dir_sizes.values())))
