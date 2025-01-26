import pathlib
import sys
import os
from typing import TypeAlias

HyperPoint: TypeAlias = tuple[int, ...]


def parse(puzzle_input: str):
    """Parse input"""
    return [tuple(int(n) for n in line.split(',')) for line in puzzle_input.split('\n')]


def distance(pt1: HyperPoint, pt2: HyperPoint) -> int:
    return sum(abs(pt1[i] - pt2[i]) for i in range(len(pt1)))


def part1(data):
    """Solve part 1"""
    num_constellations: int = 0
    while data:
        constellation: set[HyperPoint] = {data.pop()}
        while True:
            new_additions: set[HyperPoint] = set()
            for pt in data.copy():
                for c in constellation:
                    if distance(pt, c) <= 3:
                        new_additions.add(pt)
                        data.remove(pt)
                        break

            constellation.update(new_additions)
            if not new_additions:
                break

        num_constellations += 1

    return num_constellations


def part2(data):
    """Solve part 2"""
    return None


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 8
    PART2_TEST_ANSWER = None

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
