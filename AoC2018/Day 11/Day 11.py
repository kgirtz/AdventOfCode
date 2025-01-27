import pathlib
import sys
import os
import functools


def parse(puzzle_input: str):
    """Parse input"""
    return int(puzzle_input)


def power_level(x: int, y: int, grid_serial_number: int) -> int:
    rack_id: int = x + 10
    level: int = (rack_id * y + grid_serial_number) * rack_id
    return (level // 100) % 10 - 5


@functools.cache
def total_power(x: int, y: int, square_size: int, grid_serial_number: int) -> int:
    if square_size == 1:
        return power_level(x, y, grid_serial_number)

    total: int = total_power(x, y, square_size - 1, grid_serial_number)

    # Don't repeat bottom right corner
    bottom_row_y: int = y + square_size - 1
    for bottom_row_x in range(x, x + square_size):
        total += total_power(bottom_row_x, bottom_row_y, 1, grid_serial_number)

    right_side_x: int = x + square_size - 1
    for right_side_y in range(y, y + square_size - 1):
        total += total_power(right_side_x, right_side_y, 1, grid_serial_number)

    return total


def part1(data):
    """Solve part 1"""
    max_power: int = 0
    max_power_cell: tuple[int, int] = (0, 0)
    size: int = 3
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            power: int = total_power(x, y, size, data)
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
        print(size)
        for y in range(1, 302 - size):
            for x in range(1, 302 - size):
                power: int = total_power(x, y, size, data)
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
    solution2 = None#part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = (21, 61)
    PART2_TEST_ANSWER = None#(232, 251, 12)

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
