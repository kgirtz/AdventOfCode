import pathlib
import sys
import os
from typing import Iterable

from point import Point, PointTuple


class Robot:
    def __init__(self, pos: PointTuple, vel: PointTuple) -> None:
        self.position: Point = Point(*pos)
        self.velocity: Point = Point(*vel)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.position})'

    def move(self, seconds: int, width: int, height: int) -> None:
        self.position = self.velocity * seconds + self.position
        self.position = Point(self.position.x % width, self.position.y % height)

    def quadrant(self, width: int, height: int) -> int:
        middle_x: int = width // 2
        middle_y: int = height // 2
        if self.position.x > middle_x and self.position.y < middle_y:
            return 1
        if self.position.x < middle_x and self.position.y < middle_y:
            return 2
        if self.position.x < middle_x and self.position.y > middle_y:
            return 3
        if self.position.x > middle_x and self.position.y > middle_y:
            return 4


def safety_factor(robots: Iterable[Robot], width: int, height: int) -> int:
    factor: int = 1
    for quadrant in range(1, 5):
        factor *= len([r for r in robots if r.quadrant(width, height) == quadrant])
    return factor


def print_robots(robots: Iterable[Robot], width: int, height: int) -> None:
    robot_positions: set[Point] = {r.position for r in robots}
    lines: list[str] = []
    for y in range(height):
        line: str = ''
        for x in range(width):
            if (x, y) in robot_positions:
                line += '#'
            else:
                line += ' '
        lines.append(line)
    print('\n'.join(lines))


def touching(robots: Iterable[Robot]) -> int:
    robot_positions: set[Point] = {r.position for r in robots}
    return sum(len(r.position.neighbors(include_corners=True) & robot_positions) for r in robots)


def parse(puzzle_input: str):
    """Parse input"""
    robots: list[Robot] = []
    for line in puzzle_input.split('\n'):
        p_str, v_str = line.split()
        p: PointTuple = tuple(int(n) for n in p_str.removeprefix('p=').split(','))
        v: PointTuple = tuple(int(n) for n in v_str.removeprefix('v=').split(','))
        robots.append(Robot(p, v))
    return robots


def part1(data):
    """Solve part 1"""
    space_width: int = 101  # test = 11, input = 101
    space_height: int = 103  # test = 7, input = 103
    for robot in data:
        robot.move(100, space_width, space_height)
    return safety_factor(data, space_width, space_height)


def part2(data):
    """Solve part 2"""  # 6752
    space_width: int = 101
    space_height: int = 103
    for robot in data:
        robot.move(6752, space_width, space_height)
    print_robots(data, space_width, space_height)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # 12  # change size of space
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
