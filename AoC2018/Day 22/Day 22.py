import pathlib
import sys
import os
import functools
import dataclasses

from xypair import XYpair, ORIGIN


def parse(puzzle_input: str):
    """Parse input"""
    depth_str, target_str = puzzle_input.split('\n')
    depth: int = int(depth_str.split()[1])
    target: XYpair = XYpair(*(int(n) for n in target_str.split()[1].split(',')))
    return depth, target


ROCKY: int = 0
WET: int = 1
NARROW: int = 2

ALLOWED_TOOLS: dict[int, frozenset[str]] = {ROCKY: frozenset(('climbing gear', 'torch')),
                                            WET: frozenset(('climbing gear', 'neither')),
                                            NARROW: frozenset(('neither', 'torch'))}


@dataclasses.dataclass
class Cave:
    depth: int
    target: XYpair

    def __hash__(self) -> int:
        return hash((self.depth, self.target))

    @staticmethod
    def neighbors(region: XYpair) -> set[XYpair]:
        return {n for n in region.neighbors() if n.x >= 0 and n.y >= 0}

    def allowed_tools(self, region: XYpair) -> frozenset[str]:
        return ALLOWED_TOOLS[self.region_type(region)]

    @functools.cache
    def geologic_index(self, region: XYpair) -> int:
        if region == ORIGIN or region == self.target:
            return 0
        if region.y == 0:
            return region.x * 16807
        if region.x == 0:
            return region.y * 48271
        return self.erosion_level(region.left()) * self.erosion_level(region.up())

    @functools.cache
    def erosion_level(self, region: XYpair) -> int:
        return (self.geologic_index(region) + self.depth) % 20183

    @functools.cache
    def region_type(self, region: XYpair) -> int:
        return self.erosion_level(region) % 3


def part1(data):
    """Solve part 1"""
    depth, target = data

    cave: Cave = Cave(depth, target)
    risk: int = 0
    for y in range(target.y + 1):
        for x in range(target.x + 1):
            risk += cave.region_type(XYpair(x, y))
    return risk


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 114
    PART2_TEST_ANSWER = 45

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
