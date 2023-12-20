import pathlib
import sys
import os
from typing import Sequence


class Module:
    def __init__(self, name: str, destinations: Sequence[str], mod_type: str = '') -> None:
        self.name: str = name
        self.type: str = name if name == 'broadcaster' else mod_type
        self.destinations: list[str] = list(destinations)


def parse(puzzle_input):
    """Parse input"""
    modules: list[Module] = []
    for line in puzzle_input.split('\n'):
        name, destinations = line.split(' -> ')
        if name == 'broadcaster':
            modules.append(Module(name, destinations.split(', ')))
        else:
            modules.append(Module(name[1:], destinations.split(', '), name[0]))
    return modules


def part1(data):
    """Solve part 1"""
    return data


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

    PART1_TEST_ANSWER = None
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
