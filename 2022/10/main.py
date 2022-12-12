from dataclasses import dataclass


# Part 1 functions
@dataclass
class Instruction:
    name: str
    value: int | None
    cycles: int


def parse_instruction(line: str) -> Instruction:
    line = line.split()
    if line[0] == "addx":
        instruction = Instruction(line[0], int(line[1]), 2)
    elif line[0] == "noop":
        instruction = Instruction(line[0], None, 1)
    else:
        raise ValueError(f"Unknown instruction: {line[0]}")
    return instruction


def compile_(instructions: list[Instruction]) -> list[Instruction]:
    """
    "Compile" the instructions such that every instruction that takes more than
    one cycle is turned into several instructions that take exactly one cycle.
    """
    new = []
    for instruction in instructions:
        if instruction.name == "noop":
            new.append(instruction)
        elif instruction.name == "addx":
            new.append(Instruction("noop", None, 1))
            new.append(Instruction("addx", instruction.value, 1))
    return new


class Register:
    def __init__(self, start: int = 1):
        self.value = start
        self._cycles = 1  # start at 1 as want to get the value "during" a cycle

    @property
    def cycles(self) -> int:
        return self._cycles

    @property
    def signal_strength(self) -> int:
        return self.cycles * self.value

    def execute(self, instruction: Instruction):
        if instruction.name == "addx":  # "compiled" version only takes 1 cycle
            self.value += instruction.value
        self._cycles += 1


# Part 2 functions
@dataclass
class Sprite:
    pos: tuple[int, int, int]


def get_sprite(register: Register) -> Sprite:
    val = register.value
    return Sprite((val - 1, val, val + 1))


def is_lit(cycle: int, sprite: Sprite) -> bool:
    pos = cycle % 40 - 1
    if pos in sprite.pos:
        return True
    return False


def render_pixel(cycle: int, lit: bool) -> None:
    pos = cycle - 1
    if pos % 40 == 0:
        print("\n", end="", flush=True)
    if lit:
        print("#", end="", flush=True)
    else:
        print(".", end="", flush=True)


if __name__ == "__main__":
    with open("input.txt") as f:
        instructions = list(map(parse_instruction, f.readlines()))
        instructions = compile_(instructions)

    # Part 1
    cycles = [20, 60, 100, 140, 180, 220]
    strengths = []

    register = Register()
    for cycle, instruction in enumerate(instructions, start=1):
        if cycle in cycles:
            strengths.append(register.signal_strength)
        register.execute(instruction)
    print(sum(strengths))

    # Part 2
    register = Register()
    for cycle, instruction in enumerate(instructions, start=1):
        sprite = get_sprite(register)
        render_pixel(cycle, is_lit(cycle, sprite))
        register.execute(instruction)
