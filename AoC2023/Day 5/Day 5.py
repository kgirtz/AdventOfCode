import pathlib
import sys
import os
import itertools
from typing import Iterable, Sequence


class ComponentMap:
    def __init__(self, source: str, destination: str, ranges: Iterable[tuple[int, int, int]]) -> None:
        self.source: str = source
        self.destination: str = destination
        self.ranges: list[tuple[int, int, int]] = list(ranges)

    def lookup(self, n: int, *, reverse: bool = False) -> int:
        for dst, src, length in self.ranges:
            if reverse:
                dst, src = src, dst
            if src <= n < src + length:
                return n - src + dst
        return n

    def remaining_range_length(self, n: int, *, reverse: bool = False) -> int:
        for dst, src, length in self.ranges:
            if reverse:
                dst, src = src, dst
            if src <= n < src + length:
                return src + length - n
        return 1

    def merge(self, post: 'ComponentMap') -> None:
        new_ranges: list[tuple[int, int, int]] = []

        points: set[int] = set()
        for dst, _, length in self.ranges:
            points.update((dst, dst + length))
        for _, src, length in post.ranges:
            points.update((src, src + length))

        for pt1, pt2 in itertools.pairwise(sorted(points)):
            src: int = self.lookup(pt1, reverse=True)
            dst: int = post.lookup(pt1)
            if src != dst:
                new_ranges.append((dst, src, pt2 - pt1))

        self.destination = post.destination
        self.ranges = new_ranges


def parse(puzzle_input):
    """Parse input"""
    components: list[str] = puzzle_input.split('\n\n')
    seeds: list[int] = [int(n) for n in components[0].split()[1:]]

    almanac: list[ComponentMap] = []
    for component in components[1:]:
        name: str = component.split(':')[0]
        src, dest = name.split()[0].split('-to-')
        ranges: list[tuple[int, int, int]] = [tuple(int(n) for n in r.split()) for r in
                                              component.split(':')[1].strip().split('\n')]
        almanac.append(ComponentMap(src, dest, ranges))
    return seeds, almanac


def merge_maps(maps: Sequence[ComponentMap]) -> ComponentMap:
    consolidated: ComponentMap = maps[0]
    for cmap in maps[1:]:
        consolidated.merge(cmap)
    return consolidated


def part1(data):
    """Solve part 1"""
    seeds, almanac = data
    merged: ComponentMap = merge_maps(almanac)
    return min(merged.lookup(seed) for seed in seeds)


def part2(data):
    """Solve part 2"""
    seed_ranges, almanac = data
    merged: ComponentMap = merge_maps(almanac)

    location: int = 0
    while True:
        seed: int = merged.lookup(location, reverse=True)
        for i in range(0, len(seed_ranges), 2):
            start, length = seed_ranges[i:i + 2]
            if start <= seed < start + length:
                return location

        location += merged.remaining_range_length(location, reverse=True)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 35
    PART2_TEST_ANSWER = 46

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()