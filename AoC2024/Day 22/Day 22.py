import pathlib
import sys
import os
import collections
from typing import Iterable


def next_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number << 6) ^ secret_number) % 16777216
    secret_number = ((secret_number >> 5) ^ secret_number) % 16777216
    secret_number = ((secret_number << 11) ^ secret_number) % 16777216
    return secret_number


def price(secret_number: int) -> int:
    return secret_number % 10


def max_bananas(buyers: Iterable[int], iterations: int) -> int:
    bananas: dict[tuple[int, ...], int] = collections.defaultdict(int)
    for secret_number in buyers:
        cur_price: int = price(secret_number)
        price_changes: list[int] = []
        seen: set[tuple[int, ...]] = set()
        for _ in range(iterations):
            prev_price: int = cur_price
            secret_number = next_secret_number(secret_number)
            cur_price = price(secret_number)

            price_changes.append(cur_price - prev_price)
            if len(price_changes) >= 4:
                key: tuple[int, ...] = tuple(price_changes[-4:])
                if key not in seen:
                    seen.add(key)
                    bananas[key] += cur_price
    return max(bananas.values())


def parse(puzzle_input: str):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    secret_numbers: list[int] = data
    for _ in range(2000):
        secret_numbers = [next_secret_number(s) for s in secret_numbers]
    return sum(secret_numbers)


def part2(data):
    """Solve part 2"""
    return max_bananas(data, 2000)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 37327623
    PART2_TEST_ANSWER = 23

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
