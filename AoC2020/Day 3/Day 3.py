import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    lines: list[str] = puzzle_input.split('\n')
    height: int = len(lines)
    width: int = len(lines[0])
    trees: set[Point] = set()
    for y, line in enumerate(lines):
        for x, space in enumerate(line):
            if space == '#':
                trees.add(Point(x, y))
    return height, width, trees


def traverse(start: Point, del_x: int, del_y: int, width: int) -> Point:
    return Point((start.x + del_x) % width, start.y + del_y)


def trees_on_slope(origin: Point, slope: Point, trees: set[Point], height: int, width: int) -> int:
    num_trees: int = 0
    pos: Point = origin
    while pos.y < height:
        pos = traverse(pos, slope.x, slope.y, width)
        if pos in trees:
            num_trees += 1
    return num_trees


def part1(data):
    """Solve part 1"""
    height, width, trees = data
    start: Point = Point(0, 0)
    slope: Point = Point(3, 1)
    return trees_on_slope(start, slope, trees, height, width)


def part2(data):
    """Solve part 2"""
    height, width, trees = data
    start: Point = Point(0, 0)
    slopes: list[Point] = [Point(1, 1), Point(3, 1), Point(5, 1), Point(7, 1), Point(1, 2)]
    total: int = 1
    for slope in slopes:
        total *= trees_on_slope(start, slope, trees, height, width)
    return total


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
