import pathlib
import sys
import os
from typing import Iterable, NamedTuple


class Range(NamedTuple):
    dst_start: int
    src_start: int
    length: int

    def src_end(self) -> int:
        return self.src_start + self.length - 1

    def dst_end(self) -> int:
        return self.dst_start + self.length - 1

    def __contains__(self, n: int) -> bool:
        return self.src_start <= n <= self.src_end()

    def convert(self, n: int) -> int:
        return n - self.src_start + self.dst_start

    def overlaps_post(self, post: 'Range') -> bool:
        return self.dst_start in post or \
               self.dst_end() in post or \
               self.dst_start < post.src_start and self.dst_end() > post.src_end()


def collapse_ranges(pre: Range, post: list[Range]) -> list[Range]:
    new_ranges: list[Range] = []
    for r in post:
        if pre.overlaps_post(r):


    else:
        return [pre]

    return new_ranges


class Map:
    def __init__(self, source: str, destination: str, ranges: Iterable[str]) -> None:
        self.source: str = source
        self.destination: str = destination
        self.ranges: list[Range] = [Range(*(int(n) for n in r.split())) for r in ranges]

    def __getitem__(self, n: int) -> int:
        for r in self.ranges:
            if n in r:
                return r.convert(n)
        return n

    def merge(self, other: 'Map') -> None:
        if self.destination == other.source:
            pre, post = self, other
        elif other.destination == self.source:
            pre, post = other, self
        else:
            print('INVALID MAP MERGE')
            return

        pre.destination = post.destination

        new_ranges: list[Range] = []
        for r in self.ranges:
            new_ranges.extend(collapse_ranges(r, post.ranges))
        self.ranges = new_ranges

Almanac = dict[str, Map]


def parse(puzzle_input):
    """Parse input"""
    components: list[str] = puzzle_input.split('\n\n')
    seeds: list[int] = [int(n) for n in components[0].split()[1:]]

    almanac: Almanac = {}
    for component in components[1:]:
        name: str = component.split(':')[0]
        src, dest = name.split()[0].split('-to-')
        ranges: list[str] = component.split(':')[1].strip().split('\n')
        almanac[src] = Map(src, dest, ranges)
    return seeds, almanac


def look_up(n: int, source: str, destination: str, almanac: Almanac) -> int:
    print(f'look_up({n}, {source}, {destination}) = ', end='')
    while source != destination:
        source_map: Map = almanac[source]
        n = source_map[n]
        source = source_map.destination
    print(n)
    return n


def part1(data):
    """Solve part 1"""
    seeds, almanac = data
    return min(look_up(seed, 'seed', 'location', almanac) for seed in seeds)


def part2(data):
    """Solve part 2"""
    seed_ranges, almanac = data
    global_min: int = -1
    for i in range(0, len(seed_ranges), 2):
        start, length = seed_ranges[i:i + 2]
        range_min: int = min(look_up(seed, 'seed', 'location', almanac) for seed in range(start, start + length))
        if global_min == -1:
            global_min = range_min
        else:
            global_min = min(global_min, range_min)
    return global_min


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
