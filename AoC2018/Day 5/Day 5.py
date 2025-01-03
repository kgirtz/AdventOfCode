import pathlib
import sys
import os


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.strip()


def opposite_polarity(a: str, b: str) -> bool:
    return a != b and a.lower() == b.lower()


def react(polymer: str, ignore: str = '') -> str:
    ignore = ignore.lower()

    stack: list[str] = []
    for p in polymer:
        if p.lower() == ignore:
            continue

        if stack and opposite_polarity(stack[-1], p):
            stack.pop()
        else:
            stack.append(p)

    return ''.join(stack)


def part1(data):
    """Solve part 1"""
    return len(react(data))


def part2(data):
    """Solve part 2"""
    units: set[str] = {u.lower() for u in data}
    return min(len(react(data, ig)) for ig in units)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 10
    PART2_TEST_ANSWER = 4

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
