import pathlib
import sys
import os
from typing import Iterable


def parse(puzzle_input):
    """Parse input"""
    connections: dict[str, list[str]] = {}
    for line in puzzle_input.split('\n'):
        left, right = line.split(': ')
        connections[left] = right.split()
    return connections


def split_groups(connections: dict[str, list[str]], num_groups: int, num_cuts: int) -> list[set[str]]:
    all_components: Iterable[str] = set(connections.keys())
    for wires in connections.values():
        all_components |= wires
    all_components = list(all_components)

    for i, c1 in enumerate(all_components[:-2]):
        for j, c2 in enumerate(all_components[i + 1:-1]):
            for k, c3 in enumerate(all_components[j + 1:]):


    return []


def part1(data):
    """Solve part 1"""
    product: int = 1
    for group in split_groups(data,2, 3):
        product *= len(group)
    return product


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

    PART1_TEST_ANSWER = 54
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
