import pathlib
import sys
import os
from cube import Cube
from typing import Iterable
from collections import defaultdict


class Brick:
    def __init__(self, endpoint1: Cube, endpoint2: Cube) -> None:
        self.x_min: int = min(endpoint1.x, endpoint2.x)
        self.x_max: int = max(endpoint1.x, endpoint2.x)
        self.y_min: int = min(endpoint1.y, endpoint2.y)
        self.y_max: int = max(endpoint1.y, endpoint2.y)
        self.z_min: int = min(endpoint1.z, endpoint2.z)
        self.z_max: int = max(endpoint1.z, endpoint2.z)
        self.height: int = self.z_max - self.z_min

    def __repr__(self) -> str:
        return f'{self.x_min},{self.y_min},{self.z_min}~{self.x_max},{self.y_max},{self.z_max}'

    def __hash__(self) -> int:
        return hash(repr(self))

    def over(self, other: 'Brick') -> bool:
        return self.z_min > other.z_max and \
            other.x_max >= self.x_min and self.x_max >= other.x_min and \
            other.y_max >= self.y_min and self.y_max >= other.y_min

    def rests_on(self, other: 'Brick') -> bool:
        return self.over(other) and self.z_min == other.z_max + 1

    def fall(self, others: Iterable['Brick']) -> None:
        if self.z_min == 1:
            return

        for brick in sorted(others, key=lambda b: b.z_max, reverse=True):
            if self.over(brick):
                self.z_min = brick.z_max + 1
                self.z_max = self.z_min + self.height
                return

        self.z_min = 1
        self.z_max = self.height + 1


def parse(puzzle_input):
    """Parse input"""
    bricks: list[Brick] = []
    for line in puzzle_input.split('\n'):
        c1, c2 = line.split('~')
        cube1: Cube = Cube(*(int(n) for n in c1.split(',')))
        cube2: Cube = Cube(*(int(n) for n in c2.split(',')))
        bricks.append(Brick(cube1, cube2))
    return bricks


def settle(bricks: Iterable[Brick]) -> (dict[Brick, set[Brick]], dict[Brick, set[Brick]]):
    bricks: list[Brick] = sorted(bricks, key=lambda b: b.z_min)
    for i, brick in enumerate(bricks):
        brick.fall(bricks[:i])

    supports: dict[Brick, set[Brick]] = defaultdict(set)
    supported_by: dict[Brick, set[Brick]] = defaultdict(set)
    for i, top in enumerate(bricks[:-1]):
        for bottom in bricks[i + 1:]:
            if top.rests_on(bottom):
                supports[bottom].add(top)
                supported_by[top].add(bottom)
            elif bottom.rests_on(top):
                supports[top].add(bottom)
                supported_by[bottom].add(top)

    return supports, supported_by


def part1(data):
    """Solve part 1"""
    supports, supported_by = settle(data)

    can_safely_disintegrate: int = 0
    for brick in data:
        for b in supports[brick]:
            if len(supported_by[b]) == 1:
                break
        else:
            can_safely_disintegrate += 1

    return can_safely_disintegrate


def part2(data):
    """Solve part 2"""
    supports, supported_by = settle(data)

    num_falling_bricks: dict[Brick, int] = {}

    bricks: list[Brick] = sorted(data, key=lambda b: b.z_max, reverse=True)

    for i, brick in enumerate(bricks):
        falling_bricks: int = 0
        for b in supports[brick]:
            if len(supported_by[b]) == 1:
                falling_bricks += num_falling_bricks[b] + 1
        num_falling_bricks[brick] = falling_bricks

    print(sum(num_falling_bricks.values()))
    return sum(num_falling_bricks.values())


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 5
    PART2_TEST_ANSWER = 7

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
