import pathlib
import sys
import os
import functools

from xypair import XYpair, XYtuple


def parse(puzzle_input: str):
    """Parse input"""
    return int(puzzle_input)


def power_level(pt: XYpair, grid_serial_number: int) -> int:
    rack_id: int = pt.x + 10
    level: int = (rack_id * pt.y + grid_serial_number) * rack_id
    return (level % 1000) // 100 - 5


@functools.cache
def total_power(top_left: XYtuple, square_size: int, grid_serial_number: int) -> int:
    if square_size <= 1:
        top_left = XYpair(*top_left)
        rack_id: int = top_left.x + 10
        level: int = (rack_id * top_left.y + grid_serial_number) * rack_id
        return (level % 1000) // 100 - 5

    total: int = total_power(top_left, square_size - 1, grid_serial_number)
    top_left = XYpair(*top_left)

    bottom_row: int = top_left.y + square_size - 1
    for x in range(top_left.x, top_left.x + square_size):
        total += total_power(XYpair(x, bottom_row), 1, grid_serial_number)

    right_side: int = top_left.x + square_size - 1
    for y in range(top_left.y, top_left.y + square_size - 1):
        total += total_power(XYpair(right_side, y), 1, grid_serial_number)

    return total


def part1(data):
    """Solve part 1"""
    max_power: int = 0
    max_power_cell: XYpair = XYpair(0, 0)
    for y in range(1, 299):
        for x in range(1, 299):
            power: int = total_power((x, y), 3, data)
            if power > max_power:
                max_power = power
                max_power_cell = XYpair(x, y)
    return max_power_cell


def part2(data):
    """Solve part 2"""
    max_power: int = 0
    max_power_cell: XYpair = XYpair(0, 0)
    max_power_size: int = 0
    for size in range(1, 301):
        print(size)
        for y in range(1, 302 - size):
            for x in range(1, 302 - size):
                power: int = total_power((x, y), size, data)
                if power > max_power:
                    max_power = power
                    max_power_cell = XYpair(x, y)
                    max_power_size = size
    return *max_power_cell, max_power_size


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = (21, 61)
    PART2_TEST_ANSWER = (232, 251, 12)

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
