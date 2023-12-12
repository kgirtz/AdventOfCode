import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def next_num(index: int, previous: int, bank: dict[int, int]) -> int:
    if previous in bank:
        num: int = index - bank[previous]
    else:
        num = 0
    bank[previous] = index
    return num


def get_num(n: int, starting_nums: list[int]) -> int:
    bank: dict[int, int] = {n: i for i, n in enumerate(starting_nums)}
    previous: int = starting_nums[-1]
    for i in range(len(starting_nums) - 1, n - 1):
        previous = next_num(i, previous, bank)
    return previous


def part1(data):
    """Solve part 1"""
    return get_num(2020, data)


def part2(data):
    """Solve part 2"""
    return get_num(30000000, data)


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
