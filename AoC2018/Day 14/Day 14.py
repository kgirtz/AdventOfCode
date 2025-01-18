import pathlib
import sys
import os
from collections.abc import Sequence, MutableSequence


def parse(puzzle_input: str):
    """Parse input"""
    return int(puzzle_input)


def recipe_round(elf1: int, elf2: int, scoreboard: MutableSequence[int]) -> (int, int):
    recipe1: int = scoreboard[elf1]
    recipe2: int = scoreboard[elf2]
    recipe_sum: int = recipe1 + recipe2
    if recipe_sum > 9:
        scoreboard.extend((1, recipe_sum % 10))
    else:
        scoreboard.append(recipe_sum % 10)

    return (elf1 + recipe1 + 1) % len(scoreboard), (elf2 + recipe2 + 1) % len(scoreboard)


def find_at_end_of_scoreboard(seq: Sequence[int], scoreboard: Sequence[int]) -> int:
    i: int = len(scoreboard) - len(seq)
    if i < 0:
        return -1

    if i > 0 and all(a == b for a, b in zip(seq, scoreboard[i - 1:i - 1 + len(seq)])):
        return i - 1

    if all(a == b for a, b in zip(seq, scoreboard[i:i + len(seq)])):
        return i

    return -1


def part1(data):
    """Solve part 1"""
    scoreboard: list[int] = [3, 7]
    elf1: int = 0
    elf2: int = 1
    while len(scoreboard) < data + 10:
        elf1, elf2 = recipe_round(elf1, elf2, scoreboard)

    return ''.join(str(n) for n in scoreboard[data:data + 10])


def part2(data):
    """Solve part 2"""
    target: tuple[int, ...] = tuple(int(d) for d in str(data))

    scoreboard: list[int] = [3, 7]
    elf1: int = 0
    elf2: int = 1
    target_location: int = -1
    while target_location == -1:
        elf1, elf2 = recipe_round(elf1, elf2, scoreboard)
        target_location = find_at_end_of_scoreboard(target, scoreboard)

    return target_location


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = '5941429882'
    PART2_TEST_ANSWER = 2018

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
