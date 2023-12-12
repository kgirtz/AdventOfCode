import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    ranges: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for line in puzzle_input.split('\n'):
        ass1, ass2 = line.split(',')
        ass1_range: tuple[int, ...] = tuple((int(section) for section in ass1.split('-')))
        ass2_range: tuple[int, ...] = tuple((int(section) for section in ass2.split('-')))
        ranges.append((ass1_range, ass2_range))

    return ranges


def contains(r1: tuple[int, ...], r2: tuple[int, ...]) -> bool:
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def overlaps(r1: tuple[int, ...], r2: tuple[int, ...]) -> bool:
    return contains(r2, r1) or contains(r1, (r2[0], r2[0])) or contains(r1, (r2[1], r2[1]))


def part1(data):
    """Solve part 1"""

    return sum([contains(r1, r2) or contains(r2, r1) for r1, r2 in data])


def part2(data):
    """Solve part 2"""

    return sum([overlaps(r1, r2) for r1, r2 in data])


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
