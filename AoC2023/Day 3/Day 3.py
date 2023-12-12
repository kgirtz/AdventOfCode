import pathlib
import sys
import os
from typing import NamedTuple, Sequence


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split('\n')


class Gear(NamedTuple):
    x: int
    y: int
    num1: int
    num2: int

    def ratio(self) -> int:
        return self.num1 * self.num2


class Schematic:
    def __init__(self, schematic: Sequence[str]) -> None:
        self.schematic: list[str] = list(schematic)
        self.part_numbers: list[int] = []
        self.gears: set[Gear] = set()
        self.height: int = len(schematic)
        self.width: int = len(schematic[0])

        self.analyze()

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (0 <= x < self.width) and (0 <= y < self.height)

    def is_digit(self, x: int, y: int) -> bool:
        return self.is_valid_pos(x, y) and self.schematic[y][x].isdigit()

    def is_symbol(self, x: int, y: int) -> bool:
        return self.is_valid_pos(x, y) and self.schematic[y][x] != '.' and not self.is_digit(x, y)

    def start_of_num(self, x: int, y: int) -> int:
        while self.is_digit(x - 1, y):
            x -= 1
        return x

    def num_length(self, x: int, y: int) -> int:
        x = self.start_of_num(x, y)

        length: int = 0
        while self.is_digit(x + length, y):
            length += 1
        return length

    def num_at(self, x: int, y: int) -> int:
        x = self.start_of_num(x, y)

        length: int = self.num_length(x, y)
        return int(self.schematic[y][x:x + length])

    def is_part_number(self, x: int, y: int) -> bool:
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + self.num_length(x, y) + 1):
                if self.is_symbol(i, j):
                    return True
        return False

    def adjacent_numbers(self, x: int, y: int) -> list[int]:
        nums: list[int] = []

        # Before/After
        if self.is_digit(x - 1, y):
            nums.append(self.num_at(x - 1, y))
        if self.is_digit(x + 1, y):
            nums.append(self.num_at(x + 1, y))

        # Above
        if self.is_digit(x, y - 1):
            nums.append(self.num_at(x, y - 1))
        else:
            if self.is_digit(x - 1, y - 1):
                nums.append(self.num_at(x - 1, y - 1))
            if self.is_digit(x + 1, y - 1):
                nums.append(self.num_at(x + 1, y - 1))

        # Below
        if self.is_digit(x, y + 1):
            nums.append(self.num_at(x, y + 1))
        else:
            if self.is_digit(x - 1, y + 1):
                nums.append(self.num_at(x - 1, y + 1))
            if self.is_digit(x + 1, y + 1):
                nums.append(self.num_at(x + 1, y + 1))

        return nums

    def analyze(self) -> None:
        self.part_numbers = []
        for y, line in enumerate(self.schematic):
            x: int = 0
            while x < len(line):
                if self.is_digit(x, y):
                    # Identify part numbers
                    if self.is_part_number(x, y):
                        self.part_numbers.append(self.num_at(x, y))
                    x += self.num_length(x, y)
                else:
                    # Identify gears
                    if line[x] == '*':
                        adj_nums: list[int] = self.adjacent_numbers(x, y)
                        if len(adj_nums) == 2:
                            self.gears.add(Gear(x, y, adj_nums[0], adj_nums[1]))
                    x += 1


def part1(data):
    """Solve part 1"""
    schematic: Schematic = Schematic(data)
    return sum(schematic.part_numbers)


def part2(data):
    """Solve part 2"""
    schematic: Schematic = Schematic(data)
    return sum(gear.ratio() for gear in schematic.gears)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 4361
    PART2_TEST_ANSWER = 467835

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
