import pathlib
import sys
import os
import re
from collections.abc import Iterable

from xypair import XYpair


class Point:
    def __init__(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int) -> None:
        self.position: XYpair = XYpair(pos_x, pos_y)
        self.velocity: XYpair = XYpair(vel_x, vel_y)

    def position_at_time(self, t: int) -> XYpair:
        return self.position + self.velocity * t


def parse(puzzle_input: str):
    """Parse input"""
    return [Point(*(int(n) for n in re.findall(r'-?\d+', line))) for line in puzzle_input.split('\n')]


def print_points_at_time(points: Iterable[Point], t: int) -> str:
    points_at_time: frozenset[XYpair] = frozenset(point.position_at_time(t) for point in points)

    min_x: int = min(pt.x for pt in points_at_time)
    max_x: int = max(pt.x for pt in points_at_time)
    min_y: int = min(pt.y for pt in points_at_time)
    max_y: int = max(pt.y for pt in points_at_time)

    if max_y - min_y > 10:
        return ''

    lines: list[str] = []
    for y in range(min_y, max_y + 1):
        line: str = ''
        for x in range(min_x, max_x + 1):
            if (x, y) in points_at_time:
                line += '#'
            else:
                line += '.'
        lines.append(line)
    return '\n'.join(lines) + '\n'


def part1(data):
    """Solve part 1"""
    for t in range(1, 11000):
        if message := print_points_at_time(data, t):
            print(message)
            print(f'after {t} seconds')
            return


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    part1(data)


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # test = 'HI'

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solve(puzzle_input)
        print()
