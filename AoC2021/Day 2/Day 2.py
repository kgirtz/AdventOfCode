import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    horizontal_position: int = 0
    depth: int = 0

    for command in data:
        direction, distance = command.split()
        distance = int(distance)
        if direction == 'forward':
            horizontal_position += distance
        elif direction == 'up':
            depth -= distance
        elif direction == 'down':
            depth += distance

    return horizontal_position * depth


def part2(data):
    """Solve part 2"""
    horizontal_position: int = 0
    depth: int = 0
    aim: int = 0

    for command in data:
        direction, distance = command.split()
        distance = int(distance)
        if direction == 'forward':
            horizontal_position += distance
            depth += distance * aim
        elif direction == 'up':
            aim -= distance
        elif direction == 'down':
            aim += distance

    return horizontal_position * depth


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
