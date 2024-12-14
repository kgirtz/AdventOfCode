import pathlib
import sys
import os
from typing import Generator, Iterable

from point import Point
from pointwalker import PointWalker
from space import Space


class Region:
    def __init__(self, plots: Iterable[Point]) -> None:
        self.plots: set[Point] = set(plots)

    def price(self) -> int:
        return self.perimeter() * self.area()

    def bulk_price(self) -> int:
        return self.sides() * self.area()

    def area(self) -> int:
        return len(self.plots)

    def perimeter(self) -> int:
        return sum(len(pt.neighbors().difference(self.plots)) for pt in self.plots)

    def sides(self) -> int:
        sides: int = 0
        perimeter_points: set[Point] = set()
        for pt in self.plots:
            if pt.down() in self.plots or pt.down() in perimeter_points:
                continue

            # Left hand on wall
            start: PointWalker = PointWalker(pt.down(), 'EAST')
            walker: PointWalker = PointWalker(start)
            walker.track_history = True

            cur_sides: int = 0
            # while not walker.has_looped():  # TODO: bug
            while walker != start or cur_sides == 0:
                if walker.peek('LEFT') not in self.plots:
                    walker.turn('LEFT')
                    walker.step()
                    cur_sides += 1
                elif walker.next() in self.plots:
                    walker.turn('RIGHT')
                    cur_sides += 1
                else:
                    walker.step()
            perimeter_points.update(walker.visited_points())

            sides += cur_sides

        return sides


class Garden(Space):
    def expand_to_region(self, start: Point) -> Region:
        plant: str = self[start]
        seen: set[Point] = set()
        new_pts: set[Point] = {start}
        while new_pts:
            pt: Point = new_pts.pop()
            seen.add(pt)
            new_pts |= (self.neighbors(pt) & self.items[plant]) - seen
        return Region(seen)

    def regions(self) -> Generator[Region, None, None]:
        for plots in self.items.values():
            plots = set(plots)
            while plots:
                seed: Point = plots.pop()
                region: Region = self.expand_to_region(seed)
                plots -= region.plots
                yield region


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    garden: Garden = Garden(data)
    return sum(region.price() for region in garden.regions())


def part2(data):
    """Solve part 2"""
    garden: Garden = Garden(data)
    return sum(region.bulk_price() for region in garden.regions())


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
