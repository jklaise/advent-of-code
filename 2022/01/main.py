if __name__ == '__main__':

    # Part 1 - iterate over file and keep track of current highest calorie elf
    max_elf, max_calories = 0, 0
    current_elf, current_calories = 0, 0

    with open('input.txt') as f:
        for line in f:
            line = line.strip()
            if line == '':
                if current_calories > max_calories:
                    max_calories = current_calories
                    max_elf = current_elf
                current_elf += 1
                current_calories = 0
            else:
                n_calories = int(line)
                current_calories += n_calories

    print(f"{max_elf=}, {max_calories=}")

    # Part 2 - create a data structure in memory of all elves' calories
    calories = []
    current_calories = 0
    with open('input.txt') as f:
        for line in f:
            line = line.strip()
            if line == '':
                calories.append(current_calories)
                current_calories = 0
            else:
                n_calories = int(line)
                current_calories += n_calories

    # sort - O(log(n))
    calories = sorted(calories, reverse=True)
    print(sum(calories[:3]))
