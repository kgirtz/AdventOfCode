import pathlib
import sys
import os
import re
from xypair import XYpair
from typing import Sequence
from collections import defaultdict


def color_code_to_instruction(code: str) -> (str, int):
    direction: str = 'RDLU'[int(code[-1])]
    distance: int = int(code[:-1], 16)
    return direction, distance


class Lagoon:
    def __init__(self, instructions: Sequence[tuple[str, int]]) -> None:
        self.segments: list[tuple[XYpair, XYpair]] = []

        x, y = 0, 0
        for direction, distance in instructions:
            match direction:
                case 'U':
                    self.segments.append((XYpair(x, y), XYpair(x, y - distance)))
                    y -= distance
                case 'D':
                    self.segments.append((XYpair(x, y), XYpair(x, y + distance)))
                    y += distance
                case 'L':
                    self.segments.append((XYpair(x, y), XYpair(x - distance, y)))
                    x -= distance
                case 'R':
                    self.segments.append((XYpair(x, y), XYpair(x + distance, y)))
                    x += distance

    def is_s_shape(self, segment: tuple[XYpair, XYpair]) -> bool:
        if segment not in self.segments:
            segment = segment[::-1]
        segment_pos: int = self.segments.index(segment)

        prev_seg: tuple[XYpair, XYpair] = self.segments[segment_pos - 1]
        next_seg: tuple[XYpair, XYpair] = self.segments[(segment_pos + 1) % len(self.segments)]

        return (prev_seg[0].y < segment[0].y and next_seg[1].y > segment[1].y) or \
            (prev_seg[0].y > segment[0].y and next_seg[1].y < segment[1].y)

    def size(self) -> int:
        horizontal_segments: dict[int, list[tuple[int, int]]] = defaultdict(list)
        vertical_segments: list[tuple[XYpair, XYpair]] = []

        for start, end in self.segments:
            if start.x == end.x:
                top, bottom = (start, end) if start.y < end.y else (end, start)
                vertical_segments.append((top, bottom))
            else:
                left, right = (start, end) if start.x < end.x else (end, start)
                horizontal_segments[left.y].append((left.x, right.x))

        vertical_segments.sort(key=lambda pair: pair[1].y, reverse=True)

        top_row: int = min(horizontal_segments.keys())
        bottom_row: int = max(horizontal_segments.keys())

        total_area: int = 0
        row: int = top_row
        while row <= bottom_row:
            intersections: list[tuple[int, ...]] = []
            if row in horizontal_segments:
                intersections.extend(horizontal_segments[row])
            for top, bottom in vertical_segments:
                if row >= bottom.y:
                    break
                if top.y < row:
                    intersections.append((top.x,))
            intersections.sort()

            side: str = 'out'
            left_side: int = 0
            right_side: int = 0
            row_area: int = 0
            for intersection in intersections:
                # Vertical border crosses row
                if len(intersection) == 1:
                    if side == 'out':
                        left_side = intersection[0]
                        side = 'in'
                    else:
                        right_side = intersection[0]
                        side = 'out'

                # Horizontal segment in row
                else:
                    if self.is_s_shape((XYpair(intersection[0], row), XYpair(intersection[1], row))):
                        if side == 'out':
                            left_side = intersection[0]
                            side = 'in'
                        else:
                            right_side = intersection[1]
                            side = 'out'
                    elif side == 'out':
                        left_side, right_side = intersection

                if side == 'out':
                    row_area += right_side - left_side + 1

            if row not in horizontal_segments:
                num_repeated_rows: int = 0
                while row not in horizontal_segments:
                    row += 1
                    num_repeated_rows += 1
                total_area += row_area * num_repeated_rows
            else:
                row += 1
                total_area += row_area

        return total_area


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
    return Lagoon([color_code_to_instruction(color) for _, _, color in data]).size()


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

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