import pathlib
import sys
import os
import functools

from xypair import XYpair


def parse(puzzle_input: str):
    """Parse input"""
    return int(puzzle_input)


def power_level(pt: XYpair, grid_serial_number: int) -> int:
    rack_id: int = pt.x + 10
    level: int = (rack_id * pt.y + grid_serial_number) * rack_id
    return (level // 100) % 10 - 5


@functools.cache
def total_power(top_left: XYpair, bottom_right: XYpair, grid_serial_number: int) -> int:
    if bottom_right.x < top_left.x or bottom_right.y < top_left.y:
        return 0

    if top_left == bottom_right:
        return power_level(top_left, grid_serial_number)

    if top_left == (1, 1):
        return power_level(bottom_right, grid_serial_number) \
                + total_power(top_left, bottom_right.left(), grid_serial_number) \
                + total_power(top_left, bottom_right.up(), grid_serial_number) \
                - total_power(top_left, bottom_right.up_left(), grid_serial_number)

    return total_power(XYpair(1, 1), bottom_right, grid_serial_number) \
               + total_power(XYpair(1, 1), top_left.up_left(), grid_serial_number) \
               - total_power(XYpair(1, 1), XYpair(bottom_right.x, top_left.y - 1), grid_serial_number) \
               - total_power(XYpair(1, 1), XYpair(top_left.x - 1, bottom_right.y), grid_serial_number)


def prep_cache(max_size: int, grid_serial_number: int) -> None:
    for y in range(1, max_size + 1):
        for x in range(1, max_size + 1):
            total_power(XYpair(1, 1), XYpair(x, y), grid_serial_number)


def part1(data):
    """Solve part 1"""
    prep_cache(300, data)

    max_power: int = 0
    max_power_cell: tuple[int, int] = (0, 0)
    size: int = 3
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            power: int = total_power(XYpair(x, y), XYpair(x + size - 1, y + size - 1), data)
            if power > max_power:
                max_power = power
                max_power_cell = (x, y)
    return max_power_cell


def part2(data):
    """Solve part 2"""
    max_power: int = 0
    max_power_cell: tuple[int, int] = (0, 0)
    max_power_size: int = 0
    for size in range(1, 301):
        for y in range(1, 302 - size):
            for x in range(1, 302 - size):
                power: int = total_power(XYpair(x, y), XYpair(x + size - 1, y + size - 1), data)
                if power > max_power:
                    max_power = power
                    max_power_cell = (x, y)
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
