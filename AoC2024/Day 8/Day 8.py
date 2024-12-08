import pathlib
import sys
import os

from space import Space
from point import Point


class AntennaMap(Space):
    def __init__(self, input_map) -> None:
        super().__init__(input_map)

        self.locations: dict[str, set[Point]] = self.items

    def frequencies(self) -> set[str]:
        return set(self.locations.keys())

    def calculate_antinodes(self, a: Point, b: Point) -> set[Point]:
        if a == b:
            return set()

        # a to b
        rise: int = 2 * (b.y - a.y)
        run: int = 2 * (b.x - a.x)
        node_ab: Point = Point(a.x + run, a.y + rise)

        # b to a
        rise = 2 * (a.y - b.y)
        run = 2 * (a.x - b.x)
        node_ba: Point = Point(b.x + run, b.y + rise)

        return {node for node in (node_ab, node_ba) if self.valid_point(node)}

    def calculate_harmonic_antinodes(self, a: Point, b: Point) -> set[Point]:
        if a == b:
            return set()

        antinodes: set[Point] = set()

        # a to b
        rise: int = b.y - a.y
        run: int = b.x - a.x
        cur_node: Point = a

        while self.valid_point(cur_node):
            antinodes.add(cur_node)
            cur_node = Point(cur_node.x + run, cur_node.y + rise)

        cur_node = a
        while self.valid_point(cur_node):
            antinodes.add(cur_node)
            cur_node = Point(cur_node.x - run, cur_node.y - rise)

        return antinodes

    def find_antinodes(self, freq: str, *, harmonics: bool = False) -> set[Point]:
        antinodes: set[Point] = set()
        antennas: list[Point] = list(self.locations[freq])
        for i, a in enumerate(antennas[:-1]):
            for b in antennas[i + 1:]:
                if harmonics:
                    antinodes.update(self.calculate_harmonic_antinodes(a, b))
                else:
                    antinodes.update(self.calculate_antinodes(a, b))
        return antinodes


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.split('\n')


def part1(data):
    """Solve part 1"""
    antennas: AntennaMap = AntennaMap(data)
    antinodes: set[Point] = set()
    for f in antennas.frequencies():
        antinodes.update(antennas.find_antinodes(f))
    return len(antinodes)


def part2(data):
    """Solve part 2"""
    antennas: AntennaMap = AntennaMap(data)
    antinodes: set[Point] = set()
    for f in antennas.frequencies():
        antinodes.update(antennas.find_antinodes(f, harmonics=True))
    return len(antinodes)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 14
    PART2_TEST_ANSWER = 34

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
