import pathlib
import sys
import os
from typing import Sequence


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.strip().split()


def blink(stones: Sequence[str]) -> list[str]:
    new_stones: list[str] = []
    for stone in stones:
        if stone == '0':
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            new_stones.append(stone[:len(stone) // 2])
            new_stones.append(str(int(stone[len(stone) // 2:])))
        else:
            new_stones.append(str(int(stone) * 2024))
    return new_stones


def num_stones_after_blinks(stones: Sequence[str], blinks: int) -> int:
    stones = list(stones)
    for i in range(blinks):
        print(f'Blink {i + 1}')
        stones = blink(stones)
    return len(stones)


def part1(data):
    """Solve part 1"""
    return num_stones_after_blinks(data, 25)


def part2(data):
    """Solve part 2"""
    return num_stones_after_blinks(data, 75)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 55312
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
