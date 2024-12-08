import pathlib
import sys
import os

from space import Space
from point import Point


class AntennaMap(Space):
    def calculate_antinodes(self, a: Point, b: Point, harmonics: bool = False) -> set[Point]:
        if a == b:
            return set()

        antinodes: set[Point] = set()

        # a to b
        run: int = a.run(b)
        rise: int = a.rise(b)

        # Toward b
        if harmonics:
            node: Point = a
            while self.valid_point(node):
                antinodes.add(node)
                node = Point(node.x + run, node.y + rise)
        else:
            node = Point(a.x + 2 * run, a.y + 2 * rise)
            if self.valid_point(node):
                antinodes.add(node)

        # Away from b
        if harmonics:
            node = a
            while self.valid_point(node):
                antinodes.add(node)
                node = Point(node.x - run, node.y - rise)
        else:
            node: Point = Point(a.x - run, a.y - rise)
            if self.valid_point(node):
                antinodes.add(node)

        return antinodes

    def find_all_antinodes(self, *, harmonics: bool = False) -> set[Point]:
        antinodes: set[Point] = set()
        for antennas in self.items.values():
            for a in antennas:
                for b in antennas:
                    antinodes.update(self.calculate_antinodes(a, b, harmonics))
        return antinodes


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    return len(AntennaMap(data).find_all_antinodes())


def part2(data):
    """Solve part 2"""
    return len(AntennaMap(data).find_all_antinodes(harmonics=True))


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
