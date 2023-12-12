import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [[int(n) for n in list(line)] for line in puzzle_input.split('\n')]


def neighbors(x: int, y: int, height_map: list[list[int]]) -> set[tuple[int, int]]:
    potential_neighbors: list[tuple[int, int]] = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid_neighbors: set[tuple[int, int]] = set()
    for i, j in potential_neighbors:
        if 0 <= i < len(height_map) and 0 <= j < len(height_map[0]):
            valid_neighbors.add((i, j))
    return valid_neighbors


def is_low_point(x: int, y: int, height_map: list[list[int]]) -> bool:
    neighbor_heights: list[int] = [height_map[i][j] for i, j in neighbors(x, y, height_map)]
    return height_map[x][y] < min(neighbor_heights)


def low_points(height_map: list[list[int]]) -> set[tuple[int, int]]:
    points: set[tuple[int, int]] = set()
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            if is_low_point(i, j, height_map):
                points.add((i, j))
    return points


def basin_size(x: int, y: int, height_map: list[list[int]]) -> int:
    seen_so_far: set[tuple[int, int]] = set()
    to_check: set[tuple[int, int]] = {(x, y)}

    while to_check:
        x, y = to_check.pop()
        seen_so_far.add((x, y))
        for i, j in neighbors(x, y, height_map):
            if (i, j) not in seen_so_far and height_map[i][j] != 9:
                to_check.add((i, j))

    return len(seen_so_far)


def part1(data):
    """Solve part 1"""
    risk: int = 0
    for x, y in low_points(data):
        risk += data[x][y] + 1
    return risk


def part2(data):
    """Solve part 2"""
    basin_sizes: list[int] = sorted(basin_size(x, y, data) for x, y in low_points(data))
    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


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
