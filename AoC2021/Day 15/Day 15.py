import pathlib
import sys
import os
from math import inf
from queue import PriorityQueue


def parse(puzzle_input):
    """Parse input"""
    return [[int(n) for n in line] for line in puzzle_input.split()]


def neighbors(x: int, y: int, m: int) -> set[tuple[int, int]]:
    neighbor_pts: set[tuple[int, int]] = set()
    for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= i < m and 0 <= j < m:
            neighbor_pts.add((i, j))
    return neighbor_pts


def minimum_risk(risk: list[list[int]]) -> int:
    m: int = len(risk)
    lowest_risk: list[list] = [[inf for _ in range(m)] for _ in range(m)]
    lowest_risk[0][0] = 0

    visited: set[tuple[int, int]] = set()
    visit_queue: PriorityQueue[tuple[int, int, int]] = PriorityQueue()
    visit_queue.put((0, 0, 0))

    while not visit_queue.empty():
        _, x, y = visit_queue.get()
        visited.add((x, y))

        for n_x, n_y in neighbors(x, y, m):
            if (n_x, n_y) not in visited:
                old_risk: int = lowest_risk[n_y][n_x]
                new_risk: int = lowest_risk[y][x] + risk[n_y][n_x]
                if new_risk < old_risk:
                    visit_queue.put((new_risk, n_x, n_y))
                    lowest_risk[n_y][n_x] = new_risk

    return lowest_risk[-1][-1]


def expand(risk_map: list[list[int]]) -> list[list[int]]:
    m: int = len(risk_map)
    big_m: int = 5 * m
    big_map: list[list[int]] = [[0 for _ in range(big_m)] for _ in range(big_m)]
    for i in range(5):
        for j in range(5):
            for k in range(m):
                for n in range(m):
                    x: int = m * j + n
                    y: int = m * i + k
                    big_map[y][x] = risk_map[k][n] + i + j
                    while big_map[y][x] > 9:
                        big_map[y][x] -= 9
    return big_map


def part1(data):
    """Solve part 1"""
    return minimum_risk(data)


def part2(data):
    """Solve part 2"""
    expanded_data = expand(data)
    return minimum_risk(expanded_data)


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
