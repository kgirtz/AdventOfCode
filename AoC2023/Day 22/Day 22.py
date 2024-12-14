import pathlib
import sys
import os
import heapq
import functools
from xyztrio import XYZtrio
from typing import Iterable

    
class Brick:
    def __init__(self, endpoint1: XYZtrio, endpoint2: XYZtrio) -> None:
        self.x_min: int = min(endpoint1.x, endpoint2.x)
        self.x_max: int = max(endpoint1.x, endpoint2.x)
        self.y_min: int = min(endpoint1.y, endpoint2.y)
        self.y_max: int = max(endpoint1.y, endpoint2.y)
        self.z_min: int = min(endpoint1.z, endpoint2.z)
        self.z_max: int = max(endpoint1.z, endpoint2.z)
        self.height: int = self.z_max - self.z_min
        self.supports: set[Brick] = set()
        self.is_supported_by: set[Brick] = set()

    def __repr__(self) -> str:
        return f'{self.x_min},{self.y_min},{self.z_min}~{self.x_max},{self.y_max},{self.z_max}'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other) -> bool:
        return self.z_min < other.z_min

    def overlaps(self, other: 'Brick') -> bool:
        return other.x_max >= self.x_min and self.x_max >= other.x_min and \
               other.y_max >= self.y_min and self.y_max >= other.y_min

    def rests_on(self, other: 'Brick') -> bool:
        return self.z_min == other.z_max + 1 and self.overlaps(other)

    def fall(self, others: Iterable['Brick']) -> None:
        if self.z_min <= 1:
            return

        for brick in sorted(others, key=lambda b: b.z_max, reverse=True):
            if self.z_min > brick.z_max and self.overlaps(brick):
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
        cube1: XYZtrio = XYZtrio(*(int(n) for n in c1.split(',')))
        cube2: XYZtrio = XYZtrio(*(int(n) for n in c2.split(',')))
        bricks.append(Brick(cube1, cube2))
    return bricks


def settle(bricks: Iterable[Brick]) -> None:
    bricks = sorted(bricks)
    for i, brick in enumerate(bricks):
        brick.fall(bricks[:i])

    for i, bottom in enumerate(bricks[:-1]):
        for top in bricks[i + 1:]:
            if top.rests_on(bottom):
                bottom.supports.add(top)
                top.is_supported_by.add(bottom)


@functools.lru_cache(maxsize=None)
def remove_brick(brick: Brick) -> set[Brick]:
    if not brick.supports:
        return set()

    # Remove each above individually
    falling_bricks: set[Brick] = set()
    for above in brick.supports:
        if len(above.is_supported_by) == 1:
            falling_bricks.add(above)
            falling_bricks |= remove_brick(above)

    # Remove all above simultaneously
    to_check: list[Brick] = []
    for falling in falling_bricks:
        to_check.extend(falling.supports - falling_bricks)

    to_check = list(set(to_check))
    heapq.heapify(to_check)

    while to_check:
        cur_brick: Brick = heapq.heappop(to_check)
        if cur_brick.is_supported_by.issubset(falling_bricks):
            falling_bricks.add(cur_brick)
            falling_bricks |= remove_brick(cur_brick)
            for above in cur_brick.supports - falling_bricks:
                heapq.heappush(to_check, above)

    return falling_bricks


def part1(data):
    """Solve part 1"""
    settle(data)

    can_safely_disintegrate: int = 0
    for brick in data:
        if all(len(above.is_supported_by) > 1 for above in brick.supports):
            can_safely_disintegrate += 1
    return can_safely_disintegrate


def part2(data):
    """Solve part 2"""
    settle(data)

    total_falling_bricks: int = 0
    for brick in sorted(data, key=lambda b: b.z_max, reverse=True):
        total_falling_bricks += len(remove_brick(brick))
    return total_falling_bricks


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
