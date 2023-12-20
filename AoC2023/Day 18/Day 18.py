import pathlib
import sys
import os
import re
import itertools
from point import Point, ORIGIN
from typing import Sequence
from collections import defaultdict


def color_code_to_instruction(code: str) -> (str, int):
    direction: str = 'RDLU'[int(code[-1])]
    distance: int = int(code[:-1], 16)
    return direction, distance


class Lagoon:
    def __init__(self, instructions: Sequence[tuple[str, int]]) -> None:
        self.border: set[Point] = {ORIGIN}
        self.segments: set[tuple[Point, Point]] = set()
        self.horizontal_segments: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.vertical_segments: list[tuple[Point, Point]] = []

        x, y = ORIGIN
        for direction, distance in instructions:
            match direction:
                case 'U':
                    self.segments.add((Point(x, y), Point(x, y - distance)))
                    self.vertical_segments.append((Point(x, y - distance), Point(x, y)))
                case 'D':
                    self.segments.add((Point(x, y), Point(x, y + distance)))
                    self.vertical_segments.append((Point(x, y), Point(x, y + distance)))
                case 'L':
                    self.segments.add((Point(x, y), Point(x - distance, y)))
                    self.horizontal_segments[y].append((x - distance, x))
                case 'R':
                    self.segments.add((Point(x, y), Point(x + distance, y)))
                    self.horizontal_segments[y].append((x, x + distance))

            while distance > 0:
                x, y = self.next_point(Point(x, y), direction)
                self.border.add(Point(x, y))
                distance -= 1

    @staticmethod
    def next_point(pt: Point, direction: str) -> Point:
        match direction:
            case 'U':
                return pt.above()
            case 'D':
                return pt.below()
            case 'R':
                return pt.right()
            case 'L':
                return pt.left()

    def size(self) -> int:
        inside: Point = ORIGIN.up_right()
        if ORIGIN.above() in self.border:
            outside: Point = ORIGIN.up_left()
        elif ORIGIN.right() in self.border:
            outside: Point = ORIGIN.down_right()
        else:
            outside: Point = ORIGIN.down_left()

        inside_area: set[Point] = set()
        outside_area: set[Point] = set()
        inside_to_explore: set[Point] = {inside}
        outside_to_explore: set[Point] = {outside}
        while inside_to_explore and outside_to_explore:
            cur_inside: Point = inside_to_explore.pop()
            cur_outside: Point = outside_to_explore.pop()
            inside_to_explore |= cur_inside.neighbors(diagonals=True) - inside_area - self.border
            outside_to_explore |= cur_outside.neighbors(diagonals=True) - outside_area - self.border
            inside_area.add(cur_inside)
            outside_area.add(cur_outside)

        if not outside_to_explore:
            lagoon: set[Point] = self.border | outside_area
        else:
            lagoon: set[Point] = self.border | inside_area

        return len(lagoon)

    def size_smart(self) -> int:
        horizontal_lines: dict[int, list[int]] = defaultdict(list)
        for start, end in self.segments:
            horizontal_lines[start.y].append(start.x)

        for cols in horizontal_lines.values():
            cols.sort()

        lines: list[int] = sorted(horizontal_lines.keys())

        top: int = lines[0]
        bottom: int = lines[-1]

        if len(horizontal_lines[top]) != 2:
            print('PROBLEM')
            return 0

        total_size: int = 0
        for lo, hi in itertools.pairwise(lines):
            total_size += max(horizontal_lines[lo]) - min(horizontal_lines[lo]) + 1

            if len(horizontal_lines[lo]) == 2:
                left, right = horizontal_lines[lo]
            elif len(horizontal_lines) == 3:
                pass


            total_size += (lo - hi - 2) * (right - left + 1)






def parse(puzzle_input):
    """Parse input"""
    dig_plan: list[tuple[str, int, str]] = []
    for line in puzzle_input.split('\n'):
        direction, distance, color = re.match(r'(.) (.+) \(#(.+)\)', line).groups()
        dig_plan.append((direction, int(distance), color))
    return dig_plan


def part1(data):
    """Solve part 1"""
    return Lagoon([(direction, distance) for direction, distance, _ in data]).size()


def part2(data):
    """Solve part 2"""
    Lagoon([color_code_to_instruction(color) for _, _, color in data])
    return None
    return Lagoon([color_code_to_instruction(color) for _, _, color in data]).size_smart()


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = None # part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 62
    PART2_TEST_ANSWER = 952408144115

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
