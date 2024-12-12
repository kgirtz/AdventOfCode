import pathlib
import sys
import os
from typing import Collection, Generator

from point import Point
from space import Space


class Garden(Space):
    @staticmethod
    def area(region: Collection[Point]) -> int:
        return len(region)

    @staticmethod
    def perimeter(region: Collection[Point]) -> int:
        perim: int = 0
        for pt in region:
            perim += 4 - len(pt.neighbors().intersection(region))
        return perim

    @staticmethod
    def sides(region: Collection[Point]) -> int:
        sides: int = 0

        return sides

    def price(self, region: Collection[Point]) -> int:
        return self.perimeter(region) * self.area(region)

    def bulk_price(self, region: Collection[Point]) -> int:
        return self.sides(region) * self.area(region)

    def expand(self, start: Point) -> set[Point]:
        plant: str = self[start]
        pts: set[Point] = set()
        new_pts: set[Point] = {start}
        while new_pts:
            pts |= new_pts
            new_new_pts: set[Point] = set()
            for pt in new_pts:
                new_new_pts |= self.neighbors(pt) & self.items[plant]
            new_pts = new_new_pts - pts
        return pts

    def regions(self) -> Generator[set[Point], None, None]:
        for plots in self.items.values():
            plots = set(plots)
            while plots:
                seed: Point = plots.pop()
                region: set[Point] = self.expand(seed)
                plots -= region
                yield region


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    garden: Garden = Garden(data)
    return sum(garden.price(r) for r in garden.regions())


def part2(data):
    """Solve part 2"""
    garden: Garden = Garden(data)
    return sum(garden.bulk_price(r) for r in garden.regions())


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 772
    PART2_TEST_ANSWER = 436

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
