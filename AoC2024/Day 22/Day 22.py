import pathlib
import sys
import os
import collections
import functools
import itertools
from typing import Sequence, Iterable


#@functools.cache
def next_secret_number(secret_number: int, iterations: int = 1) -> int:
    for i in range(iterations):
        secret_number = prune((secret_number << 6) ^ secret_number)
        secret_number = prune((secret_number >> 5) ^ secret_number)
        secret_number = prune((secret_number << 11) ^ secret_number)
    return secret_number


def prune(num: int) -> int:
    return num % 16777216


#@functools.cache
def price(secret_number: int) -> int:
    return secret_number % 10


def build_map_changes_to_bananas(secret_number: int, iterations: int) -> dict[tuple[int, ...], int]:
    mapping: dict[tuple[int, ...], int] = {}
    cur_price: int = price(secret_number)
    history: collections.deque[int] = collections.deque()
    for _ in range(iterations):
        prev_price: int = cur_price
        secret_number = next_secret_number(secret_number)
        cur_price = price(secret_number)

        history.append(cur_price - prev_price)
        if len(history) > 4:
            history.popleft()

        if len(history) == 4:
            key: tuple[int, ...] = tuple(history)
            if key not in mapping:
                mapping[key] = cur_price
    return mapping


def bananas_gotten(target_changes: Sequence[int], prices: list[int]) -> int:
#def bananas_gotten(target_changes: Sequence[int], secret_number: int, max_iterations: int) -> int:
    target_changes = collections.deque(target_changes)
    change_history: collections.deque[int] = collections.deque()
    """prev_price: int = price(secret_number)
    for _ in range(max_iterations):
        secret_number = next_secret_number(secret_number)
        cur_price: int = price(secret_number)"""
    #prev_price: int = prices[0]
    #for cur_price in prices[1:]:
    for prev_price, cur_price in itertools.pairwise(prices):
        change_history.append(cur_price - prev_price)
        if len(change_history) > 4:
            change_history.popleft()
        if change_history == target_changes:
            return cur_price

        #prev_price = cur_price

    return 0


def max_bananas_gotten(buyers: Iterable[int], max_iterations: int) -> int:
    prices: list[list[int]] = []
    for buyer in buyers:
        buyer_prices: list[int] = [buyer]
        for _ in range(max_iterations):
            buyer = next_secret_number(buyer)
            buyer_prices.append(buyer)
        prices.append(buyer_prices)

    return sum(bananas_gotten([-2,1,-1,3], buyer) for buyer in prices)

    #best_time: list[int] = []
    max_bananas: int = 0
    for first in range(-9, 10):
        for second in range(-9, 10):
            print(second)
            for third in range(-9, 10):
                for fourth in range(-9, 10):
                    changes: list[int] = [first, second, third, fourth]
                    bananas: int = sum(bananas_gotten(changes, buyer) for buyer in prices)
                    if bananas > max_bananas:
                        max_bananas = bananas
                        #best_time = changes
    return max_bananas


def parse(puzzle_input: str):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    return sum(next_secret_number(buyer, 2000) for buyer in data)


def part2(data):
    """Solve part 2"""
    mappings: list[dict[tuple[int, ...], int]] = [build_map_changes_to_bananas(buyer, 2000) for buyer in data]
    possibilities: set[tuple[int, ...]] = set()
    for m in mappings:
        possibilities.update(m.keys())

    return max(sum(m.get(p, 0) for m in mappings) for p in possibilities)


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
