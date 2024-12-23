import pathlib
import sys
import os
import functools


def parse(puzzle_input: str):
    """Parse input"""
    towels_str, patterns_str = puzzle_input.split('\n\n')
    towels: frozenset[str] = frozenset(towels_str.split(', '))
    patterns: list[str] = patterns_str.split('\n')
    return towels, patterns


@functools.cache
def possible(pattern: str, towels: frozenset[str]) -> int:
    num_matches: int = 0
    if pattern in towels:
        num_matches += 1
    for i in range(1, len(pattern)):
        if pattern[:i] in towels:
            num_matches += possible(pattern[i:], towels)
    return num_matches


def part1(data):
    """Solve part 1"""
    towels, patterns = data
    return sum(bool(possible(pattern, towels)) for pattern in patterns)


def part2(data):
    """Solve part 2"""
    towels, patterns = data
    return sum(possible(pattern, towels) for pattern in patterns)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 6
    PART2_TEST_ANSWER = 16

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
