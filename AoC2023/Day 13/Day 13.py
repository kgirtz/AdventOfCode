import pathlib
import sys
import os
from point import Point
from collections import defaultdict


class Pattern:
    UNKNOWN = 0
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, pattern: list[str]) -> None:
        self.height: int = len(pattern)
        self.width: int = len(pattern[0])
        self.columns: dict[int, set[int]] = defaultdict(set)
        self.rows: dict[int, set[int]] = defaultdict(set)
        self.reflection_direction: int = self.UNKNOWN
        self.reflection_line: int = -1

        for y, line in enumerate(pattern):
            for x, space in enumerate(line):
                if space == '#':
                    self.columns[x].add(y)
                    self.rows[y].add(x)

        self.find_reflection_line()

    def valid_vertical_reflecting_line(self, left: int) -> bool:
        right: int = left + 1
        while 0 <= left and right < self.width:
            if self.columns[left] != self.columns[right]:
                return False
            left -= 1
            right += 1
        return True

    def valid_horizontal_reflecting_line(self, above: int) -> bool:
        below: int = above + 1
        while 0 <= above and below < self.height:
            if self.rows[above] != self.rows[below]:
                return False
            above -= 1
            below += 1
        return True

    def find_reflection_line(self) -> None:
        for midpoint in range(self.width - 1):
            if self.valid_vertical_reflecting_line(midpoint):
                self.reflection_direction = self.VERTICAL
                self.reflection_line = midpoint
                return

        for midpoint in range(self.height - 1):
            if self.valid_horizontal_reflecting_line(midpoint):
                self.reflection_direction = self.HORIZONTAL
                self.reflection_line = midpoint
                return

        print('FAILED TO FIND LINE')

    def fix_smudge(self) -> None:
        pass


def parse(puzzle_input):
    """Parse input"""
    return [Pattern(pattern.split('\n')) for pattern in puzzle_input.split('\n\n')]


def part1(data):
    """Solve part 1"""
    return sum(pattern.reflection_line + 1 for pattern in data if pattern.reflection_direction == Pattern.VERTICAL) + \
            100 * sum(pattern.reflection_line + 1 for pattern in data if pattern.reflection_direction == Pattern.HORIZONTAL)


def part2(data):
    """Solve part 2"""
    for pattern in data:
        pattern.fix_smudge()

    return sum(pattern.reflection_line + 1 for pattern in data if pattern.reflection_direction == 'VERTICAL') + \
        100 * sum(pattern.reflection_line + 1 for pattern in data if pattern.reflection_direction == 'HORIZONTAL')


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 405
    PART2_TEST_ANSWER = 400

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
