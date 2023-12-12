import pathlib
import sys
import os
from collections import namedtuple, defaultdict

Point = namedtuple('Point', ['x', 'y'])
line_segment = tuple[Point, Point]


def parse_line(line: str) -> line_segment:
    point1, point2 = (pair.split(',') for pair in line.split('->'))
    return Point(int(point1[0]), int(point1[1])),  Point(int(point2[0]), int(point2[1]))


def parse(puzzle_input):
    """Parse input"""
    return {parse_line(line) for line in puzzle_input.split('\n')}


def points_on_segment(ends: line_segment, diag: bool = False) -> set[Point]:
    p1, p2 = ends
    points: set[Point] = set()

    if p1.x == p2.x:
        start: int = min(p1.y, p2.y)
        end: int = max(p1.y, p2.y)
        for y in range(start, end + 1):
            points.add((p1.x, y))
    elif p1.y == p2.y:
        start = min(p1.x, p2.x)
        end = max(p1.x, p2.x)
        for x in range(start, end + 1):
            points.add((x, p1.y))
    elif diag:
        if (p1.x - p2.x) * (p1.y - p2.y) > 0:  # upper left to lower right
            y: int = min(p1.y, p2.y)
            y_mod: int = 1
        else:  # lower left to upper right
            y = max(p1.y, p2.y)
            y_mod = -1

        x: int = min(p1.x, p2.x)
        end = max(p1.x, p2.x)
        while x <= end:
            points.add((x, y))
            x += 1
            y += y_mod

    return points


def part1(data):
    """Solve part 1"""
    vents: defaultdict[Point, int] = defaultdict(int)
    for segment in data:
        for pt in points_on_segment(segment):
            vents[pt] += 1

    danger_points: list[Point] = [pt for pt, count in vents.items() if count > 1]
    return len(danger_points)


def part2(data):
    """Solve part 2"""
    vents: defaultdict[Point, int] = defaultdict(int)
    for segment in data:
        for pt in points_on_segment(segment, True):
            vents[pt] += 1

    danger_points: list[Point] = [pt for pt, count in vents.items() if count > 1]
    return len(danger_points)


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
