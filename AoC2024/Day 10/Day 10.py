import pathlib
import sys
import os

from space import Space
from point import Point


class TopoMap(Space):
    def trailheads(self) -> set[Point]:
        return self.items['0']

    def score(self, trailhead: Point) -> int:
        assert self[trailhead] == 0

        cur_lvl: set[Point] = {trailhead}
        for lvl in range(1, 10):
            next_lvl: set[Point] = set()
            for pt in cur_lvl:
                next_lvl |= self.neighbors(pt) & self.items[str(lvl)]
            cur_lvl = next_lvl
        return len(cur_lvl)

    def rating(self, trailhead: Point) -> int:
        assert self[trailhead] == 0

        cur_paths: set[tuple[Point, ...]] = {(trailhead,)}
        for lvl in range(1, 10):
            next_paths: set[tuple[Point, ...]] = set()
            for path in cur_paths:
                next_paths |= {path + (n,) for n in self.neighbors(path[-1]) & self.items[str(lvl)]}
            cur_paths = next_paths
        return len(cur_paths)


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    topo: TopoMap = TopoMap(data)
    topo.integer_values = True
    return sum(topo.score(trail) for trail in topo.trailheads())


def part2(data):
    """Solve part 2"""
    topo: TopoMap = TopoMap(data)
    topo.integer_values = True
    return sum(topo.rating(trail) for trail in topo.trailheads())


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 36
    PART2_TEST_ANSWER = 81

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
