import pathlib
import sys
import os
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    line = puzzle_input.split('\n')[0]
    return [int(position) for position in line.split(',')]


def init_positions(crabs: list[int]) -> dict[int, int]:
    initial_positions: defaultdict[int, int] = defaultdict(int)
    for pos in crabs:
        initial_positions[pos] += 1
    return dict(initial_positions)


def fuel_burned_pt1(distance: int) -> int:
    return distance


def fuel_burned_pt2(distance: int) -> int:
    return distance * (distance + 1) // 2


def total_fuel_consumption(position: int, counts: dict[int, int], burn_rate: callable) -> int:
    consumed: int = 0
    for pos, count in counts.items():
        consumed += count * burn_rate(abs(position - pos))
    return consumed


def part1(data):
    """Solve part 1"""
    positions: dict[int, int] = init_positions(data)
    start: int = min(positions.keys())
    end: int = max(positions.keys())

    min_fuel: int = 10 ** 100
    for pos in range(start, end + 1):
        min_fuel = min(min_fuel, total_fuel_consumption(pos, positions, fuel_burned_pt1))

    return min_fuel


def part2(data):
    """Solve part 2"""
    positions: dict[int, int] = init_positions(data)
    start: int = min(positions.keys())
    end: int = max(positions.keys())

    min_fuel: int = 10 ** 100
    for pos in range(start, end + 1):
        min_fuel = min(min_fuel, total_fuel_consumption(pos, positions, fuel_burned_pt2))

    return min_fuel


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
