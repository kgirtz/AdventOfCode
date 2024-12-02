import pathlib
import sys
import os
import itertools
from typing import Sequence


def parse(puzzle_input: str):
    """Parse input"""
    reports: list[str] = puzzle_input.split('\n')
    return [[int(lvl) for lvl in report.split()] for report in reports]


def is_safe(report: Sequence[int]) -> bool:
    return all(1 <= b - a <= 3 for a, b in itertools.pairwise(report)) or \
           all(1 <= a - b <= 3 for a, b in itertools.pairwise(report))


def is_safe_with_dampener(report: Sequence[int]) -> bool:
    report = list(report)
    return any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report)))


def part1(data):
    """Solve part 1"""
    return sum(is_safe(report) for report in data)


def part2(data):
    """Solve part 2"""
    return sum(is_safe_with_dampener(report) for report in data)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 2
    PART2_TEST_ANSWER = 4

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
