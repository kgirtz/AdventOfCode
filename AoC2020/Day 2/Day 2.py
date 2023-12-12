import pathlib
import sys
import os
import parse as scanf


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    num_valid: int = 0
    for line in data:
        min_count, max_count, ch, password = scanf.parse('{:d}-{:d} {}: {}', line)
        if min_count <= password.count(ch) <= max_count:
            num_valid += 1
    return num_valid


def part2(data):
    """Solve part 2"""
    num_valid: int = 0
    for line in data:
        pos1, pos2, ch, password = scanf.parse('{:d}-{:d} {}: {}', line)
        if (password[pos1 - 1] == ch) ^ (password[pos2 - 1] == ch):
            num_valid += 1
    return num_valid


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
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
