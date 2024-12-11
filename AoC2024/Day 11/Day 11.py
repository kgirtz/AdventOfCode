import pathlib
import sys
import os
import functools


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.strip().split()


@functools.cache
def num_stones(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1

    blinks -= 1
    if stone == '0':
        return num_stones('1', blinks)
    elif len(stone) % 2 == 0:
        half: int = len(stone) // 2
        return num_stones(stone[:half], blinks) + num_stones(str(int(stone[half:])), blinks)
    else:
        return num_stones(str(int(stone) * 2024), blinks)


def part1(data):
    """Solve part 1"""
    return sum(num_stones(stone, 25) for stone in data)


def part2(data):
    """Solve part 2"""
    return sum(num_stones(stone, 75) for stone in data)


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
