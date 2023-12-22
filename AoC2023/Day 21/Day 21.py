import pathlib
import sys
import os
from typing import Sequence
from point import Point
from collections import defaultdict


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

    def possible_destinations(self, num_steps: int) -> int:
        cur_points: dict[Point, int] = {self.start: 1}
        for _ in range(num_steps):
            new_points: dict[Point, int] = defaultdict(int)
            for pt, num in cur_points.items():
                for neighbor in pt.neighbors():
                    if self.valid_point(neighbor):
                        new_points[neighbor] = num
                    else:
                        neighbor = Point(neighbor.x % self.width, neighbor.y % self.height)
                        new_points[neighbor] += 1
            cur_points = {pt: num for pt, num in new_points.items() if pt not in self.rocks}
            print(cur_points)
        print(sum(cur_points.values()))
        return sum(cur_points.values())


def parse(puzzle_input):
    """Parse input"""
    return Garden(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    return data.possible_destinations(num_steps=64)  # test = 6, input = 64


def part2(data):
    """Solve part 2"""
    return data.possible_destinations(num_steps=10)  # test.txt: 5000, input = 26501365


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = None  # part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # test = 16, input = None
    PART2_TEST_ANSWER = 50  # test = 16733044, input = None

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