import pathlib
import sys
import os
from collections import namedtuple
from math import atan

Point = namedtuple('Point', 'x y')

sys.path.append('..')
from intcode import IntcodeComputer


class TractorBeamDroid:
    def __init__(self, program: list[int]) -> None:
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program
        self.beam: set[Point] = set()

    def point_in_beam(self, x: int, y: int) -> bool:
        if (x, y) in self.beam:
            return True
        return self.computer.execute(self.program, [x, y]) == [1]

    def square_fits_in_beam(self, x: int, y: int, n: int) -> bool:
        return self.point_in_beam(x + n - 1, y) and self.point_in_beam(x, y + n - 1)

    def scan_area(self, height: int, width: int) -> None:
        x_min: int = 0
        for y in range(height):
            found_beam: bool = False
            for x in range(x_min, width):
                # In beam
                if self.point_in_beam(x, y):
                    if not found_beam:
                        x_min = x

                    self.beam.add(Point(x, y))
                    found_beam = True
                # Beyond far edge of beam
                elif found_beam:
                    break

    def find_closest_square(self, n: int) -> Point:
        # Determine starting position
        lo_y: int = max(pt.y for pt in self.beam)
        hi_x: int = max(pt.x for pt in self.beam)

        lo_points: set[Point] = {pt for pt in self.beam if pt.y == lo_y}
        hi_points: set[Point] = {pt for pt in self.beam if pt.x == hi_x}

        lo_x: int = min(pt.x for pt in lo_points)
        hi_y: int = min(pt.y for pt in hi_points)

        lo_slope: float = lo_y / lo_x
        hi_slope: float = hi_y / hi_x

        excess_y: float = hi_slope * n * hi_slope

        x_min: int = int((n + excess_y) / (lo_slope - hi_slope)) - 1

        y: int = int(hi_slope * x_min + excess_y) - 1
        while True:
            found_beam: bool = False
            x = x_min
            while True:
                if not found_beam and not self.point_in_beam(x, y):
                    x += 1
                    continue
                if not found_beam:
                    x_min = x
                    found_beam = True

                if not self.point_in_beam(x + n - 1, y):
                    break

                if self.point_in_beam(x, y + n - 1):
                    return Point(x, y)

                x += 1
            y += 1


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    droid: TractorBeamDroid = TractorBeamDroid(data)
    droid.scan_area(50, 50)
    return len(droid.beam)


def part2(data):
    """Solve part 2"""
    droid: TractorBeamDroid = TractorBeamDroid(data)
    droid.scan_area(75, 75)
    closest_pt: Point = droid.find_closest_square(100)
    return closest_pt.x * 10000 + closest_pt.y


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
