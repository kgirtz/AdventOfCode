import pathlib
import sys
import os
from collections.abc import Sequence


def parse(puzzle_input: str):
    """Parse input"""
    return [int(n) for n in puzzle_input.split()]


class Node:
    def __init__(self, nums: Sequence[int]) -> None:
        num_children: int = nums[0]
        self.children: list[Node] = []

        i: int = 2
        for _ in range(num_children):
            self.children.append(Node(nums[i:]))
            i += len(self.children[-1])

        num_metadata: int = nums[1]
        self.metadata: tuple[int, ...] = tuple(nums[i:i + num_metadata])

    def __len__(self) -> int:
        return 2 + len(self.metadata) + sum(len(child) for child in self.children)

    def metadata_sum(self) -> int:
        return sum(self.metadata) + sum(child.metadata_sum() for child in self.children)

    def value(self) -> int:
        if not self.children:
            return sum(self.metadata)

        total: int = 0
        for i in self.metadata:
            if 0 < i <= len(self.children):
                total += self.children[i - 1].value()
        return total


def part1(data):
    """Solve part 1"""
    return Node(data).metadata_sum()


def part2(data):
    """Solve part 2"""
    return Node(data).value()


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 138
    PART2_TEST_ANSWER = 66

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
