import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    count: int = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            count += 1
    return count


def part2(data):
    """Solve part 2"""
    return part1([sum(data[i:i + 3]) for i in range(len(data) - 2)])


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
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
