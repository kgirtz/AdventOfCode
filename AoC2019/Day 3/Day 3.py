import pathlib
import sys
import os
from collections import namedtuple
from typing import Optional

Point = namedtuple('Point', 'x y')
Segment = tuple[Point, Point]


def parse(puzzle_input):
    """Parse input"""
    return [line.split(',') for line in puzzle_input.split('\n')]


def build_wire(directions: list[str]) -> list[Segment]:
    segments: list[Segment] = []
    cur_pos: Point = Point(0, 0)
    endpoint: Point = cur_pos
    for move in directions:
        direction, distance = move[0], int(move[1:])

        if direction == 'U':
            endpoint = Point(cur_pos.x, cur_pos.y + distance)
        elif direction == 'D':
            endpoint = Point(cur_pos.x, cur_pos.y - distance)
        elif direction == 'L':
            endpoint = Point(cur_pos.x - distance, cur_pos.y)
        elif direction == 'R':
            endpoint = Point(cur_pos.x + distance, cur_pos.y)

        segments.append((cur_pos, endpoint))
        cur_pos = endpoint

    return segments


def vertical(seg: Segment) -> bool:
    return seg[0].x == seg[1].x


def horizontal(seg: Segment) -> bool:
    return seg[0].y == seg[1].y


def intersects(seg1: Segment, seg2: Segment) -> Optional[Point]:
    if (vertical(seg1) and vertical(seg2)) or (horizontal(seg1) and horizontal(seg2)):
        return None

    if vertical(seg1):
        vert, horiz = seg1, seg2
    else:
        vert, horiz = seg2, seg1

    top: int = max(pt.y for pt in vert)
    bottom: int = min(pt.y for pt in vert)
    left: int = min(pt.x for pt in horiz)
    right: int = max(pt.x for pt in horiz)

    if bottom <= horiz[0].y <= top and left <= vert[0].x <= right:
        return Point(vert[0].x, horiz[0].y)
    else:
        return None


def intersections(wire1: list[Segment], wire2: list[Segment]) -> set[Point]:
    origin: Point = Point(0, 0)
    crossovers: set[Point] = set()
    for s1 in wire1:
        for s2 in wire2:
            crossover_pt: Optional[Point] = intersects(s1, s2)
            if crossover_pt is not None and crossover_pt != origin:
                crossovers.add(crossover_pt)
    return crossovers


def distance_to_origin(pt: Point) -> int:
    return abs(pt.x) + abs(pt.y)


def on_segment(pt: Point, seg: Segment) -> bool:
    if vertical(seg):
        top: int = max(pt.y for pt in seg)
        bottom: int = min(pt.y for pt in seg)
        return pt.x == seg[0].x and bottom <= pt.y <= top
    else:
        right: int = max(pt.x for pt in seg)
        left: int = min(pt.x for pt in seg)
        return pt.y == seg[0].y and left <= pt.x <= right


def steps_to_point(pt: Point, segments: list[Segment]) -> int:
    steps: int = 0
    for seg in segments:
        if on_segment(pt, seg):
            if vertical(seg):
                steps += abs(seg[0].y - pt.y)
            else:
                steps += abs(seg[0].x - pt.x)
            break
        else:
            if vertical(seg):
                steps += abs(seg[0].y - seg[1].y)
            else:
                steps += abs(seg[0].x - seg[1].x)
    return steps


def part1(data):
    """Solve part 1"""
    wire1: list[Segment] = build_wire(data[0])
    wire2: list[Segment] = build_wire(data[1])
    return min(distance_to_origin(pt) for pt in intersections(wire1, wire2))


def part2(data):
    """Solve part 2"""
    wire1: list[Segment] = build_wire(data[0])
    wire2: list[Segment] = build_wire(data[1])
    crossovers: set[Point] = intersections(wire1, wire2)
    return min(steps_to_point(pt, wire1) + steps_to_point(pt, wire2) for pt in crossovers)


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
