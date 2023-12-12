import pathlib
import sys
import os

sys.path.append('..')
from intcode import IntcodeComputer


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    computer = IntcodeComputer()
    if len(data) > 12:
        computer.execute(data, noun=12, verb=2)
    else:
        computer.execute(data)
    return computer.memory[0]


def part2(data):
    """Solve part 2"""
    computer: IntcodeComputer = IntcodeComputer()
    for noun in range(100):
        for verb in range(100):
            computer.execute(data, noun=noun, verb=verb)
            if computer.memory[0] == 19690720:
                return 100 * noun + verb


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):  # 'example.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
