import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y z')


def parse(puzzle_input):
    """Parse input"""
    return {Point(*(int(c) for c in line.split(','))) for line in puzzle_input.split('\n')}


def neighbors(pt: Point) -> set[Point]:
    return {Point(pt.x - 1, pt.y, pt.z), Point(pt.x + 1, pt.y, pt.z),
            Point(pt.x, pt.y - 1, pt.z), Point(pt.x, pt.y + 1, pt.z),
            Point(pt.x, pt.y, pt.z - 1), Point(pt.x, pt.y, pt.z + 1)}


def against_drops(pt: Point, drops: set[Point]) -> bool:
    touching: set[Point] = neighbors(pt)
    if touching & drops:
        return True

    for t in touching:
        if neighbors(t) & drops:
            return True

    return False


def shell(pt: Point, drops: set[Point]) -> set[Point]:
    shell_pts: set[Point] = set()
    edge_pts: set[Point] = {pt}
    seen: set[Point] = set()

    while edge_pts:
        new_edge_pts: set[Point] = set()
        for pt in edge_pts:
            touching: set[Point] = neighbors(pt)
            new_edge_pts |= touching
            if touching & drops:
                shell_pts.add(pt)

        seen |= edge_pts
        edge_pts = new_edge_pts - edge_pts - shell_pts - drops - seen
        edge_pts = {pt for pt in edge_pts if against_drops(pt, drops)}

    return shell_pts


def part1(data):
    """Solve part 1"""
    exposed_sides: int = 0
    for cube in data:
        exposed_sides += len(neighbors(cube) - data)

    return exposed_sides


def part2(data):
    """Solve part 2"""
    min_x_point: Point = min(data)
    outer_shell_pt: Point = Point(min_x_point.x - 1, min_x_point.y, min_x_point.z)

    air_shell: set[Point] = shell(outer_shell_pt, data)

    exposed_sides: int = 0
    for cube in data:
        exposed_sides += len(neighbors(cube) & air_shell)

    return exposed_sides


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
