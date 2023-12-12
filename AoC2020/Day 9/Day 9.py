import pathlib
import sys
import os
from typing import Optional


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def valid(n: int, window: list[int]) -> bool:
    for i, a in enumerate(window[:-1]):
        for b in window[i + 1:]:
            if a != b and a + b == n:
                return True
    return False


def first_invalid(stream: list[int], window_size: int) -> Optional[int]:
    first, last = 0, window_size
    for i, n in enumerate(stream[window_size:], window_size):
        if not valid(n, stream[first:last]):
            return stream[i]
        first += 1
        last += 1


def sum_run(stream: list[int], n: int) -> tuple[int, int]:
    first, last = 0, 0
    total: int = stream[0]
    while first < len(stream):
        if total == n:
            break
        while total < n:
            last += 1
            total += stream[last]
        if total == n:
            break
        while total > n:
            total -= stream[first]
            first += 1
    return first, last


def part1(data):
    """Solve part 1"""
    return first_invalid(data, 25)


def part2(data):
    """Solve part 2"""
    invalid: int = part1(data)
    first, last = sum_run(data, invalid)
    run: list[int] = data[first:last + 1]
    return min(run) + max(run)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
