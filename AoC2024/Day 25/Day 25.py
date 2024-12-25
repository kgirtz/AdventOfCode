import pathlib
import sys
import os
from typing import Sequence


def parse(puzzle_input: str):
    """Parse input"""
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    for grid in puzzle_input.split('\n\n'):
        rows: list[str] = grid.split('\n')
        top_row: str = rows[0]
        width: int = len(top_row)
        heights: list[int] = [[line[i] for line in rows].count('#') - 1 for i in range(width)]
        if set(top_row) == {'#'}:
            locks.append(heights)
        else:
            keys.append(heights)
    return locks, keys


def fits(key: Sequence[int], lock: Sequence[int]) -> bool:
    return all(k + l <= 5 for k, l in zip(key, lock, strict=True))


def part1(data):
    """Solve part 1"""
    locks, keys = data
    return sum(fits(key, lock) for lock in locks for key in keys)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    return solution1,


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 3

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
