import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [[int(value) for value in line.split()] for line in puzzle_input.split('\n')]


def next_value(history: list[int]) -> int:
    if len(set(history)) == 1:
        return history[-1]

    delta: list[int] = [history[i] - history[i - 1] for i in range(1, len(history))]
    return history[-1] + next_value(delta)


def previous_value(history: list[int]) -> int:
    if len(set(history)) == 1:
        return history[0]

    delta: list[int] = [history[i] - history[i - 1] for i in range(1, len(history))]
    return history[0] - previous_value(delta)


def part1(data):
    """Solve part 1"""
    return sum(next_value(history) for history in data)


def part2(data):
    """Solve part 2"""
    return sum(previous_value(history) for history in data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 114
    PART2_TEST_ANSWER = 2

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
