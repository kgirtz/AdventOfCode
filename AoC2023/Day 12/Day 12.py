import pathlib
import sys
import os
import re
from typing import Sequence


def parse(puzzle_input):
    """Parse input"""
    data: list[tuple[list[str], list[int]]] = []
    for line in puzzle_input.split('\n'):
        springs, groups = line.split()
        data.append((re.findall(r'[?#]+', springs), [int(g) for g in groups.split(',')]))
    return data


def possible_positions(spring: str, chunks: Sequence[int]) -> int:
    if len(spring) < chunk:
        return 0
    if len(spring) == chunk or spring.count('#') == chunk:
        return 1


def possible_arrangements(springs: Sequence[str], groups: Sequence[int]) -> int:
    if not springs or not groups:
        return 0

    if len(springs) == len(groups):
        return max(len(springs[0]) - groups[0] + 1, 0) * possible_arrangements(springs[1:], groups[1:])

    if len(springs) < len(groups):



    return 0


def part1(data):
    """Solve part 1"""
    print(data)
    return sum(possible_arrangements(springs, groups) for springs, groups in data)


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 21
    PART2_TEST_ANSWER = None

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
