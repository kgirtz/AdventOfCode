import pathlib
import sys
import os
import functools
import math
from typing import Sequence


def parse(puzzle_input):
    """Parse input"""
    data: list[tuple[list[str], list[int]]] = []
    for line in puzzle_input.split('\n'):
        springs, groups = line.split()
        data.append((springs, [int(g) for g in groups.split(',')]))
    return data


def combos(chunk_len: int, groups: Sequence[int]) -> int:
    extra_space: int = chunk_len - (sum(groups) + len(groups) - 1)
    if extra_space < 0:
        return 0

    return math.factorial(len(groups) + extra_space) // math.factorial(len(groups)) // math.factorial(extra_space)


@functools.lru_cache(maxsize=None)
def possible_arrangements(line: str, groups: tuple[int, ...]) -> int:
    if not groups:
        return 0 if '#' in line else 1
    
    line = line.lstrip('.')
    if not line:
        return 0

    chunk: str = line.split('.', 1)[0]

    if '#' in chunk:
        if len(chunk) < groups[0]:
            return 0

        if len(chunk) == groups[0]:
            return possible_arrangements(line[groups[0] + 1:], groups[1:])

        # len(chunk) > groups[0]
        if chunk.startswith('#'):
            if chunk[groups[0]] == '#':
                return 0
            return possible_arrangements(line[groups[0] + 1:], groups[1:])

        # line starts with '?'
        return possible_arrangements(line[1:], groups) + possible_arrangements('#' + line[1:], groups)

    else:
        if len(chunk) < groups[0]:
            return possible_arrangements(line[len(chunk):], groups)

        arrangements: int = possible_arrangements(line[len(chunk):], groups)
        for i, group in enumerate(groups):
            if sum(groups[:i + 1]) + i > len(chunk):
                break
            arrangements += combos(len(chunk), groups[:i + 1]) * possible_arrangements(line[len(chunk):], groups[i + 1:])
        return arrangements


def unfold(springs: str, groups: Sequence[int]) -> (list, tuple[int, ...]):
    return '?'.join([springs] * 5), tuple(groups) * 5


def part1(data):
    """Solve part 1"""
    return sum(possible_arrangements(springs, tuple(groups)) for springs, groups in data)


def part2(data):
    """Solve part 2"""
    return sum(possible_arrangements(*unfold(springs, groups)) for springs, groups in data)


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
    PART2_TEST_ANSWER = 525152

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