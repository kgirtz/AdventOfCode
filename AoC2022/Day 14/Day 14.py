import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    lines: list[str] = puzzle_input.split('\n')
    return [[Point(*(int(c) for c in rock.split(','))) for rock in line.split(' -> ')] for line in lines]


def build_rock_formation(scan: list[list[Point]]) -> set[Point]:
    formation: set[Point] = set()

    for line in scan:
        for i, pt in enumerate(line[:-1]):
            end: Point = line[i + 1]
            if pt.x == end.x:
                for y in range(min(pt.y, end.y), max(pt.y, end.y) + 1):
                    formation.add(Point(pt.x, y))
            else:
                for x in range(min(pt.x, end.x), max(pt.x, end.x) + 1):
                    formation.add(Point(x, pt.y))
        formation.add(line[-1])

    return formation


def lowest_rock(scan: list[list[Point]]) -> int:
    return max(max(pt.y for pt in line) for line in scan)


def fall_one_space(pt: Point, rocks: set[Point], sand: set[Point]) -> Point:
    target_d: Point = Point(pt.x, pt.y + 1)
    target_dl: Point = Point(pt.x - 1, pt.y + 1)
    target_dr: Point = Point(pt.x + 1, pt.y + 1)

    open_targets: set[Point] = {target_d, target_dl, target_dr} - sand - rocks

    if target_d in open_targets:
        return target_d
    if target_dl in open_targets:
        return target_dl
    if target_dr in open_targets:
        return target_dr
    return pt


def part1(data):
    """Solve part 1"""
    formation: set[Point] = build_rock_formation(data)
    abyss_level: int = lowest_rock(data)
    sand_source: Point = Point(500, 0)
    sand: set[Point] = set()

    falling_in_abyss: bool = False
    while not falling_in_abyss:
        sand_unit: Point = sand_source
        while True:
            fall_target: Point = fall_one_space(sand_unit, formation, sand)

            # Check if at rest
            if fall_target == sand_unit:
                sand.add(sand_unit)
                break

            # Check if in abyss
            if fall_target.y >= abyss_level:
                falling_in_abyss = True
                break

            sand_unit = fall_target

    return len(sand)


def part2(data):
    """Solve part 2"""
    formation: set[Point] = build_rock_formation(data)
    floor_level: int = lowest_rock(data) + 2
    sand_source: Point = Point(500, 0)
    sand: set[Point] = set()

    while sand_source not in sand:
        sand_unit: Point = sand_source
        while True:
            fall_target: Point = fall_one_space(sand_unit, formation, sand)

            # Check if at rest or on floor
            if fall_target == sand_unit or fall_target.y == floor_level:
                sand.add(sand_unit)
                break

            sand_unit = fall_target

    return len(sand)


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
