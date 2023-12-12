import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def fuel_required(mass: int) -> int:
    return mass // 3 - 2


def fuel_required_compound(mass: int) -> int:
    fuel: int = fuel_required(mass)
    if fuel <= 0:
        return 0
    return fuel + fuel_required_compound(fuel)


def part1(data):
    """Solve part 1"""
    return sum(fuel_required(mass) for mass in data)


def part2(data):
    """Solve part 2"""
    return sum(fuel_required_compound(mass) for mass in data)


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
