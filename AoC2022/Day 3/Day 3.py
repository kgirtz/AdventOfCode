import pathlib
import sys
import os

priority: dict[str, int] = {chr(ord('a') + i): i + 1 for i in range(26)}
priority.update({chr(ord('A') + i): i + 1 + 26 for i in range(26)})


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split('\n')


def part1(data):
    """Solve part 1"""
    priority_sum: int = 0
    for sack in data:
        comp_size: int = len(sack) >> 1  # len / 2
        common_items: set[str] = set(sack[:comp_size]) & set(sack[comp_size:])

        if len(common_items) == 1:
            priority_sum += priority[common_items.pop()]
        else:
            print("More than 1 shared item!")

    return priority_sum


def part2(data):
    """Solve part 2"""
    priority_sum: int = 0
    for i in range(0, len(data), 3):
        badge: set[str] = set(data[i]) & set(data[i + 1]) & set(data[i + 2])

        if len(badge) == 1:
            priority_sum += priority[badge.pop()]
        else:
            print("More than 1 badge!")

    return priority_sum


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
