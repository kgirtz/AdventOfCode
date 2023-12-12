import pathlib
import sys
import os
import re


def parse(puzzle_input):
    """Parse input"""
    point_list, instructions = puzzle_input.split('\n\n')
    points: set[tuple[int, int]] = {tuple(int(n) for n in line.split(',')) for line in point_list.split()}
    folds: list[tuple[str, int]] = []
    for inst in instructions.split('\n'):
        direction, position = scanf.parse('fold along {}={:d}', inst)
        folds.append((direction, position))
    return points, folds


def fold(points: set[tuple[int, int]], instruction: tuple[str, int]) -> set[tuple[int, int]]:
    direction, fold_line = instruction
    new_points: set[tuple[int, int]] = set()
    for x, y in points:
        if (direction == 'y' and y < fold_line) or (direction == 'x' and x < fold_line):
            new_points.add((x, y))
        elif direction == 'y':
            new_points.add((x, 2 * fold_line - y))
        elif direction == 'x':
            new_points.add((2 * fold_line - x, y))
    return new_points


def print_page(points: set[tuple[int, int]]) -> None:
    max_x: int = max(x for x, _ in points)
    max_y: int = max(y for _, y in points)
    for j in range(max_y + 1):
        for i in range(max_x + 1):
            if (i, j) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(data):
    """Solve part 1"""
    points, folds = data
    return len(fold(points, folds[0]))


def part2(data):
    """Solve part 2"""
    points, folds = data
    for f in folds:
        points = fold(points, f)
    print_page(points)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    part2(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
