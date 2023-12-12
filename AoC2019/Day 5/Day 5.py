import pathlib
import sys
import os

sys.path.append('..')
from intcode import IntcodeComputer


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    computer: IntcodeComputer = IntcodeComputer()
    computer.execute(data, [1])
    return computer.output


def part2(data):
    """Solve part 2"""
    computer: IntcodeComputer = IntcodeComputer()
    computer.execute(data, [5])
    return computer.output


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
