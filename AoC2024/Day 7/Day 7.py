import pathlib
import sys
import os
import itertools
import functools
from typing import Sequence, Callable, Iterable
from operator import add, mul


@functools.cache
def concat(a: int, b: int, /) -> int:
    return int(str(a) + str(b))


def parse(puzzle_input: str):
    """Parse input"""
    equations: list[str] = puzzle_input.split('\n')
    test_values: list[int] = [int(e.split(':')[0]) for e in equations]
    remaining: list[tuple[int, ...]] = [tuple(int(n) for n in e.split(':')[1].split()) for e in equations]
    return zip(test_values, remaining)


def evaluates_to(nums: Sequence[int], ops: Sequence[Callable[[int, int], int]], test_value: int) -> bool:
    value: int = nums[0]
    for num, op in zip(nums[1:], ops, strict=True):
        if value > test_value:
            break
        value = op(value, num)
    return value == test_value


def could_be_true(test_value: int, nums: Sequence[int], ops: Iterable[Callable]) -> bool:
    num_ops: int = len(nums) - 1
    return any(evaluates_to(nums, combo, test_value) for combo in itertools.product(ops, repeat=num_ops))


def could_be_true_optimized(test_value: int, nums: Sequence[int], ops: Iterable[Callable]) -> bool:
    num_ops: int = len(nums) - 1

    if mul in ops and test_value % nums[-1] != 0:
        if concat in ops and not str(test_value).endswith(str(nums[-1])):
            for combo in itertools.product(ops, repeat=num_ops):
                if combo[-1] not in (mul, concat) and evaluates_to(nums, combo, test_value):
                    return True
            return False

        for combo in itertools.product(ops, repeat=num_ops):
            if combo[-1] != mul and evaluates_to(nums, combo, test_value):
                return True
        return False

    if concat in ops and not str(test_value).endswith(str(nums[-1])):
        for combo in itertools.product(ops, repeat=num_ops):
            if combo[-1] != concat and evaluates_to(nums, combo, test_value):
                return True
        return False

    for combo in itertools.product(ops, repeat=num_ops):
        if evaluates_to(nums, combo, test_value):
            return True
    return False


def part1(data):
    """Solve part 1"""
    return sum(tv for tv, nums in data if could_be_true(tv, nums, (add, mul)))


def part2(data):
    """Solve part 2"""
    return sum(tv for tv, nums in data if could_be_true_optimized(tv, nums, (add, mul, concat)))


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 3749
    PART2_TEST_ANSWER = 11387

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
