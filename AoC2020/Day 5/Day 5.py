import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def row_number(boarding_pass: str) -> int:
    low, high = 0, 127
    for partition in boarding_pass[:7]:
        if partition == 'F':
            high = (high - low) // 2 + low
        else:
            low = (high - low) // 2 + low + 1
    return low


def column_number(boarding_pass: str) -> int:
    left, right = 0, 7
    for partition in boarding_pass[7:]:
        if partition == 'L':
            right = (right - left) // 2 + left
        else:
            left = (right - left) // 2 + left + 1
    return left


def seat_id(boarding_pass: str) -> int:
    return 8 * row_number(boarding_pass) + column_number(boarding_pass)


def part1(data):
    """Solve part 1"""
    return max(seat_id(bp) for bp in data)


def part2(data):
    """Solve part 2"""
    if len(data) > 1:
        ids: list[int] = sorted(seat_id(bp) for bp in data)
        for i, id in enumerate(ids):
            if id + 1 != ids[i + 1]:
                return id + 1


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
