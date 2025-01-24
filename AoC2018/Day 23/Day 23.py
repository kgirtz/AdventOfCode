import pathlib
import sys
import os
import dataclasses

from xyztrio import XYZtrio


@dataclasses.dataclass
class Nanobot:
    position: XYZtrio
    signal_radius: int

    def in_range(self, pt: XYZtrio) -> bool:
        return self.position.manhattan_distance(pt) <= self.signal_radius


def parse(puzzle_input: str):
    """Parse input"""
    nanobots: list[Nanobot] = []
    for line in puzzle_input.split('\n'):
        pos_str, r_str = line.split('>, ')
        pos: XYZtrio = XYZtrio(*(int(n) for n in pos_str.lstrip('pos=<').split(',')))
        r: int = int(r_str.lstrip('r='))
        nanobots.append(Nanobot(pos, r))
    return nanobots


def part1(data):
    """Solve part 1"""
    strongest: Nanobot = max(data, key=lambda n: n.signal_radius)
    return sum(strongest.in_range(n.position) for n in data)


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

    PART1_TEST_ANSWER = 7
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
