import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    for i, n in enumerate(data):
        for m in data[i + 1:]:
            if n + m == 2020:
                return n * m


def part2(data):
    """Solve part 2"""
    for i, n in enumerate(data):
        for j, m in enumerate(data[i + 1:]):
            for k in data[j + 1:]:
                if n + m + k == 2020:
                    return n * m * k


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
