def read_input(filename: str) -> list:
    with open(filename) as f:
        data = list(map(int, f.readlines()))

    return data


def find_indices(data: list, sum_to: int) -> tuple:
    for i, num1 in enumerate(data):
        for j, num2 in enumerate(data[i + 1 :]):
            if num1 + num2 == sum_to:
                return i, i + j + 1


def find_indices3(data: list, sum_to: int) -> tuple:
    for i, num1 in enumerate(data):
        for j, num2 in enumerate(data[i + 1 :]):
            for k, num3 in enumerate(data[i + j + 1 :]):
                if num1 + num2 + num3 == sum_to:
                    return i, i + j + 1, i + j + k + 1


if __name__ == "__main__":
    data = read_input("input.txt")
    i, j = find_indices(data, sum_to=2020)
    print(f"Product of two is {data[i]*data[j]}")

    i, j, k = find_indices3(data, sum_to=2020)
    print(f"Product of three is {data[i]*data[j]*data[k]}")
