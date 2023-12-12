import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [[int(n) for n in g.split()] for g in puzzle_input.split('\n\n')]


def count_calories(calories: list[list[int]]) -> list[int]:
    for cal in calories:
        yield sum(cal)


def part1(data):
    """Solve part 1"""

    return max(count_calories(data))


def part2(data):
    """Solve part 2"""
    a: int = 0
    b: int = 0
    c: int = 0
    for cal in count_calories(data):
        if cal > a:
            a, b, c = cal, a, b
        elif cal > b:
            b, c = cal, b
        elif cal > c:
            c = cal

    return sum((a, b, c))


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
