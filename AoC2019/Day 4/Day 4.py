import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split('-')]


def viable(password: int) -> bool:
    twins: bool = False
    digit: int = password % 10
    remainder: int = password // 10

    while remainder:
        next_digit: int = remainder % 10

        if next_digit > digit:
            return False
        if next_digit == digit:
            twins = True

        digit = next_digit
        remainder //= 10

    return twins


def viable_limit_twins(password: int) -> bool:
    twins: bool = False
    run_len: int = 1
    digit: int = password % 10
    remainder: int = password // 10

    while remainder:
        next_digit: int = remainder % 10

        if next_digit > digit:
            return False

        if next_digit == digit:
            run_len += 1
        elif run_len == 2:
            twins = True
            run_len = 1
        else:
            run_len = 1

        digit = next_digit
        remainder //= 10

    if run_len == 2:
        twins = True

    return twins


def part1(data):
    """Solve part 1"""
    start, end = data

    assert viable(111111)
    assert not viable(223450)
    assert not viable(123789)

    num_viable: int = 0
    for password in range(start, end + 1):
        if viable(password):
            num_viable += 1
    return num_viable


def part2(data):
    """Solve part 2"""
    start, end = data

    assert viable_limit_twins(112233)
    assert not viable_limit_twins(123444)
    assert viable_limit_twins(111122)

    num_viable: int = 0
    for password in range(start, end + 1):
        if viable_limit_twins(password):
            num_viable += 1
    return num_viable


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
