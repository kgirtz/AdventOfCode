import pathlib
import sys
import os
import re

from point import Point, ORIGIN


def parse(puzzle_input: str):
    """Parse input"""
    claw_machines: list[tuple[Point, Point, Point]] = []
    for m in puzzle_input.split('\n\n'):
        numbers: list[int] = [int(n) for n in re.findall(r'\d+', m)]
        a: Point = Point(*numbers[0:2])
        b: Point = Point(*numbers[2:4])
        prize: Point = Point(*numbers[4:6])
        claw_machines.append((a, b, prize))
    return claw_machines


def min_cost(a: Point, b: Point, prize: Point, start: Point = ORIGIN) -> int:
    b_numerator: int = a.x * prize.y - a.y * prize.x
    b_denominator: int = a.x * b.y - a.y * b.x
    if b_numerator % b_denominator:
        return -1

    b_presses: int = b_numerator // b_denominator
    if (prize.x - b.x * b_presses) % a.x:
        return -1

    a_presses: int = (prize.x - b.x * b_presses) // a.x
    return 3 * a_presses + b_presses


def part1(data):
    """Solve part 1"""
    total_cost: int = 0
    for a, b, prize in data:
        cost: int = min_cost(a, b, prize)
        if cost != -1:
            total_cost += cost
    return total_cost


def part2(data):
    """Solve part 2"""
    total_cost: int = 0
    for a, b, prize in data:
        cost: int = min_cost(a, b, Point(prize.x + 10000000000000, prize.y + 10000000000000))
        if cost != -1:
            total_cost += cost
    return total_cost


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 480
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
