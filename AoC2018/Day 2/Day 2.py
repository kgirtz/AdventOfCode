import pathlib
import sys
import os
from collections import Counter
from collections.abc import Collection


def has_copies(s: str, copy_count: int) -> bool:
    return copy_count in Counter(s).values()


def checksum(id_list: Collection) -> int:
    two_copies: int = sum(has_copies(i, 2) for i in id_list)
    three_copies: int = sum(has_copies(i, 3) for i in id_list)
    return two_copies * three_copies


def single_difference(s1: str, s2: str) -> int | None:
    assert s1 != s2 and len(s1) == len(s2)

    difference: int = -1
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            if difference != -1:
                return None
            difference = i
    return difference


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.split()


def part1(data):
    """Solve part 1"""
    return checksum(data)


def part2(data):
    """Solve part 2"""
    for i, s1 in enumerate(data[:-1]):
        for s2 in data[i + 1:]:
            diff: int | None = single_difference(s1, s2)
            if diff is not None:
                return s1[:diff] + s1[diff + 1:]


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 12
    PART2_TEST_ANSWER = 'fgij'

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
