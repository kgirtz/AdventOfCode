import pathlib
import sys
import os
from typing import Sequence
from point import Point


class Garden:
    def __init__(self, garden_map: Sequence[str]) -> None:
        self.height: int = len(garden_map)
        self.width: int = len(garden_map[0])
        self.rocks: set[Point] = set()
        self.start: Point = Point()

        for y, line in enumerate(garden_map):
            for x, plot in enumerate(line):
                if plot == 'S':
                    self.start = Point(x, y)
                elif plot == '#':
                    self.rocks.add(Point(x, y))

    def valid_point(self, pt: Point) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def take_steps(self, num_steps: int) -> list[Point]:
        cur_points: set[Point] = {self.start}


        return list(cur_points)


def parse(puzzle_input):
    """Parse input"""
    return Garden(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    return len(data.take_steps(6))


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = None  # part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 16
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
