import pathlib
import sys
import os
from collections import deque


def parse(puzzle_input):
    """Parse input"""
    line = puzzle_input.split('\n')[0]
    return [int(timer) for timer in line.split(',')]


def init_population(fish_list: list[int]) -> deque[int]:
    population: deque[int] = deque([0] * 9)
    for n in fish_list:
        population[n] += 1
    return population


def simulate_day(population: deque[int]) -> None:
    reproducing: int = population.popleft()
    population.append(reproducing)
    population[6] += reproducing


def simulate_n_days(population: deque[int], n: int) -> None:
    for _ in range(n):
        simulate_day(population)


def part1(data):
    """Solve part 1"""
    population: deque[int] = init_population(data)
    simulate_n_days(population, 80)
    return sum(population)


def part2(data):
    """Solve part 2"""
    population: deque[int] = init_population(data)
    simulate_n_days(population, 256)
    return sum(population)


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
