from operator import eq, xor


def read_input(filename: str) -> list:
    lows, highs, letters, passwords = [], [], [], []
    with open(filename) as f:
        for line in f:
            lowhigh, letter, password = line.split()
            low, high = lowhigh.split("-")
            letter = letter.replace(":", "")
            lows.append(int(low))
            highs.append(int(high))
            letters.append(letter)
            passwords.append(password)

    return lows, highs, letters, passwords


def ge_and_le(x: int, low: int, high: int) -> bool:
    return (x >= low) and (x <= high)


def count_valid(lows: list, highs: list, letters: list, passwords: list) -> int:
    return sum(map(ge_and_le, map(str.count, passwords, letters), lows, highs))


def count_valid_new(pos1: list, pos2: list, letters: list, passwords: list) -> int:
    return sum(
        xor(pwd[p1 - 1] == letter, pwd[p2 - 1] == letter)
        for p1, p2, letter, pwd in zip(pos1, pos2, letters, passwords)
    )


if __name__ == "__main__":
    # part 1
    lows, highs, letters, passwords = read_input("input.txt")
    valid_passwords = count_valid(lows, highs, letters, passwords)
    print(f"Number of valid passwords: {valid_passwords}")

    # part 2
    pos1, pos2 = lows, highs
    valid_passwords = count_valid_new(pos1, pos2, letters, passwords)
    print(f"Number of valid passwords (part 2): {valid_passwords}")