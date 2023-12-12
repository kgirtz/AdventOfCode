import pathlib
import sys
import os

MAX_ENERGY = 9


def parse(puzzle_input):
    """Parse input"""
    return [[int(n) for n in list(line)] for line in puzzle_input.split('\n')]


def print_map(energy: list[list[int]]) -> None:
    for row in energy:
        print(''.join(str(n) for n in row))
    print()


def valid(x: int, y: int, energy: list[list[int]]) -> bool:
    return 0 <= x < len(energy) and 0 <= y < len(energy[0])


def flash_ready(energy: list[list[int]]) -> bool:
    for i in range(len(energy)):
        for j in range(len(energy[0])):
            if energy[i][j] > MAX_ENERGY:
                return True
    return False


def flash(x: int, y: int, energy: list[list[int]]) -> None:
    neighbors: list[tuple[int, int]] = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                        (x, y - 1),                 (x, y + 1),
                                        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    for i, j in neighbors:
        if valid(i, j, energy):
            energy[i][j] += 1
    energy[x][y] = -100


def step(energy_map: list[list[int]]) -> int:
    for i in range(len(energy_map)):
        for j in range(len(energy_map[0])):
            energy_map[i][j] += 1

    num_flashes: int = 0
    while flash_ready(energy_map):
        for i in range(len(energy_map)):
            for j in range(len(energy_map[0])):
                if energy_map[i][j] > MAX_ENERGY:
                    flash(i, j, energy_map)
                    num_flashes += 1

    for i in range(len(energy_map)):
        for j in range(len(energy_map[0])):
            energy_map[i][j] = max(0, energy_map[i][j])

    return num_flashes


def part1(data):
    """Solve part 1"""
    flashes: int = 0
    # print_map(data)
    for _ in range(100):
        flashes += step(data)
        # print_map(data)
    return flashes


def part2(data):
    """Solve part 2"""
    for s in range(500):
        if step(data) == len(data) ** 2:
            return s + 1


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
