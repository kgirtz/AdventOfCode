import pathlib
import sys
import os
from typing import Sequence
from xypair import XYpair
from collections import defaultdict


class Contraption:
    DEFLECT: dict[str, dict[str, str]] = {'/': {'^': '>',
                                                'v': '<',
                                                '<': 'v',
                                                '>': '^'},
                                          '\\': {'^': '<',
                                                 'v': '>',
                                                 '<': '^',
                                                 '>': 'v'}
                                          }
    SPLIT: dict[str, list[str]] = {'|': ['^', 'v'],
                                   '-': ['<', '>']}

    def __init__(self, floor: Sequence[str]) -> None:
        self.height: int = len(floor)
        self.width: int = len(floor[0])
        self.obstacles: dict[XYpair, str] = {}

        for y, line in enumerate(floor):
            for x, square in enumerate(line):
                if square != '.':
                    self.obstacles[XYpair(x, y)] = square

    def valid_point(self, pt: XYpair) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def passes_through(self, pt: XYpair, direction: str) -> bool:
        match self.obstacles.get(pt, '.'):
            case '.':
                return True
            case '|':
                return direction in ('^', 'v')
            case '-':
                return direction in ('<', '>')
            case _:
                return False

    def propagate_beam(self, cur_pos: XYpair, direction: str) -> (XYpair, list[str]):
        match direction:
            case '^':
                next_pos: XYpair = cur_pos.up()
            case 'v':
                next_pos: XYpair = cur_pos.down()
            case '<':
                next_pos: XYpair = cur_pos.left()
            case '>':
                next_pos: XYpair = cur_pos.right()
            case _:
                print('INVALID DIRECTION')
                raise

        if not self.valid_point(next_pos):
            return next_pos, []

        if self.passes_through(next_pos, direction):
            return next_pos, [direction]

        # Split or deflect
        obstacle: str = self.obstacles[next_pos]
        match obstacle:
            case '|' | '-':
                return next_pos, self.SPLIT[obstacle]
            case '/' | '\\':
                return next_pos, [self.DEFLECT[obstacle][direction]]

    def energize(self, start_pos: XYpair, start_dir: str) -> list[XYpair]:
        beams: list[tuple[XYpair, str]] = [(start_pos, start_dir)]
        energized: dict[XYpair, set[str]] = defaultdict(set)
        while beams:
            new_beams: list[tuple[XYpair, str]] = []
            for pos, direction in beams:
                if pos in energized and direction in energized[pos]:
                    continue

                if self.valid_point(pos):
                    energized[pos].add(direction)

                next_beam, next_directions = self.propagate_beam(pos, direction)
                for nd in next_directions:
                    new_beams.append((next_beam, nd))

            beams = new_beams

        return list(energized.keys())


def parse(puzzle_input):
    """Parse input"""
    return Contraption(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    return len(data.energize(XYpair(-1, 0), '>'))


def part2(data):
    """Solve part 2"""
    max_energy: int = 0
    for x in range(data.width):
        max_energy = max(max_energy, len(data.energize(XYpair(x, -1), 'v')), len(data.energize(XYpair(x, data.height), '^')))
    for y in range(data.height):
        max_energy = max(max_energy, len(data.energize(XYpair(-1, y), '>')), len(data.energize(XYpair(data.width, y), '<')))
    return max_energy


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 46
    PART2_TEST_ANSWER = 51

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
