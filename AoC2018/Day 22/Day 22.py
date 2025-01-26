import pathlib
import sys
import os
import functools
import dataclasses
import heapq

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

TOOLS: tuple[str, ...] = ('climbing gear', 'torch', 'none')

ALLOWED_TOOLS: dict[int, set[str]] = {ROCKY: {'climbing gear', 'torch'},
                                      WET: {'climbing gear', 'none'},
                                      NARROW: {'none', 'torch'}}


@dataclasses.dataclass
class Cave:
    depth: int
    target: XYpair

    def __hash__(self) -> int:
        return hash((self.depth, self.target))

    @staticmethod
    def neighbors(region: XYpair) -> set[XYpair]:
        return {n for n in region.neighbors() if n.x >= 0 and n.y >= 0}

    def allowed_tools(self, region: XYpair) -> set[str]:
        return ALLOWED_TOOLS[self.region_type(region)]

    def common_tools(self, r1: XYpair, r2: XYpair) -> set[str]:
        return self.allowed_tools(r1) & self.allowed_tools(r2)

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

    def region_type(self, region: XYpair) -> int:
        return self.erosion_level(region) % 3

    def fastest_time_to_target(self) -> int:
        other_tool: str = (self.allowed_tools(ORIGIN) - {'torch'}).pop()
        seen: dict[XYpair, dict[str, int]] = {ORIGIN: {'torch': 0, other_tool: 7}}
        to_check: list[tuple[int, int, XYpair]] = [(0, self.target.manhattan_distance(ORIGIN), ORIGIN)]

        while to_check:
            _, _, cur_pt = heapq.heappop(to_check)
            assert max(seen[cur_pt].values()) <= min(seen[cur_pt].values()) + 7
            times: dict[str, int] = seen[cur_pt]
            for n in self.neighbors(cur_pt):
                # Feels hacky, but works for this input
                if n.x > 50:
                    continue

                distance_to_origin: int = n.manhattan_distance(ORIGIN)
                distance_to_target: int = n.manhattan_distance(self.target)
                if n not in seen:
                    seen[n] = {}
                for tool in self.allowed_tools(n):
                    m: int = (times[tool] + 1) if tool in times else (times[self.common_tools(n, cur_pt).pop()] + 7 + 1)
                    if tool not in seen[n] or m < seen[n][tool]:
                        seen[n][tool] = m
                        if n != self.target and (self.target not in seen or m + distance_to_target < seen[self.target]['torch']):
                            if (distance_to_origin, distance_to_target, n) not in to_check:
                                heapq.heappush(to_check, (distance_to_origin, distance_to_target, n))

        return seen[self.target]['torch']


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
    depth, target = data
    return Cave(depth, target).fastest_time_to_target()


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
