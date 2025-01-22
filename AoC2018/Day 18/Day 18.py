import pathlib
import sys
import os

from xypair import XYpair
from space import Space


class Forest(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.trees: set[XYpair] = self.items['|']
        self.lumberyards: set[XYpair] = self.items['#']

    def minute(self) -> None:
        new_trees: set[XYpair] = self.trees.copy()
        new_lumberyards: set[XYpair] = self.lumberyards.copy()

        open_acres: set[XYpair] = set()
        for tree in self.trees:
            open_acres.update(self.neighbors(tree, include_corners=True))
        open_acres -= self.trees | self.lumberyards

        for acre in open_acres:
            if len(acre.neighbors(include_corners=True) & self.trees) >= 3:
                new_trees.add(acre)

        for acre in self.trees:
            if len(acre.neighbors(include_corners=True) & self.lumberyards) >= 3:
                new_lumberyards.add(acre)
                new_trees.remove(acre)

        for acre in self.lumberyards:
            adjacent_acres: set[XYpair] = acre.neighbors(include_corners=True)
            if not (len(adjacent_acres & self.lumberyards) >= 1 and len(adjacent_acres & self.trees) >= 1):
                new_lumberyards.remove(acre)

        self.trees = self.items['|'] = new_trees
        self.lumberyards = self.items['#'] = new_lumberyards

    def resource_value(self) -> int:
        return len(self.trees) * len(self.lumberyards)

    def state(self) -> (frozenset[XYpair], frozenset[XYpair]):
        return frozenset(self.trees), frozenset(self.lumberyards)

    def minutes_pass(self, num_minutes: int) -> None:
        seen: dict[tuple[frozenset[XYpair], frozenset[XYpair]], int] = {}
        for m in range(num_minutes):
            seen[self.state()] = m

            self.minute()

            if self.state() in seen:
                startup: int = seen[self.state()]
                cycle_length: int = m - startup + 1
                reduced_minutes: int = (num_minutes - startup) % cycle_length
                return self.minutes_pass(reduced_minutes)


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    forest: Forest = Forest(data)
    forest.minutes_pass(10)
    return forest.resource_value()


def part2(data):
    """Solve part 2"""
    forest: Forest = Forest(data)
    forest.minutes_pass(1000000000)
    return forest.resource_value()


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 1147
    PART2_TEST_ANSWER = None

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
