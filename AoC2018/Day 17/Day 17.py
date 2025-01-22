import pathlib
import sys
import os
from collections.abc import Iterable

from xypair import XYpair, XYtuple


class Ground:
    def __init__(self, clay: Iterable[tuple[int, ...]]) -> None:
        self.min_y: int = min(y for _, _, y, _ in clay)
        self.max_y: int = max(y for _, _, _, y in clay)
        self.settled_water: set[XYpair] = set()
        self.moving_water: set[XYpair] = set()
        self.clay: set[XYpair] = set()
        for x_min, x_max, y_min, y_max in clay:
            self.clay.update(XYpair(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1))
        self.spill_points: set[XYpair] = set()
    
    def produce_water(self, source: XYtuple) -> None:
        obstacles: set[XYpair] = self.clay | self.settled_water
        cur_pos: XYpair = XYpair(*source)
        self.spill_points.add(cur_pos)
        spill_pos: XYpair = XYpair(-1, -1)
        while True:
            self.moving_water.add(cur_pos)
            
            # Fall
            if cur_pos.down() not in obstacles:
                cur_pos = cur_pos.down()
                if cur_pos.y > self.max_y:
                    return
                continue
            
            # Spread left
            left_falls: bool = False
            left_pos: XYpair = cur_pos
            while left_pos.left() not in self.clay:
                left_pos = left_pos.left()
                if left_pos.down() not in obstacles:
                    left_falls = True
                    break
            
            # Spread right
            right_falls: bool = False
            right_pos: XYpair = cur_pos
            while right_pos.right() not in self.clay:
                right_pos = right_pos.right()
                if right_pos.down() not in obstacles:
                    right_falls = True
                    break
            
            layer: set[XYpair] = {XYpair(x, cur_pos.y) for x in range(left_pos.x, right_pos.x + 1)}
            
            # Fill resevoir
            if not left_falls and not right_falls:
                self.settled_water.update(layer)
                obstacles.update(layer)
                cur_pos = cur_pos.up()
                continue
            
            if cur_pos == spill_pos:
                return
            spill_pos = cur_pos
            self.moving_water.update(layer)
            
            # Spill over left and/or right
            if left_falls and left_pos not in self.spill_points:
                self.produce_water(left_pos)
            if right_falls and right_pos not in self.spill_points:
                self.produce_water(right_pos)
            
            while cur_pos in self.settled_water:
                cur_pos = cur_pos.up()
            
    def all_water(self) -> set[XYpair]:
        return {w for w in self.settled_water | self.moving_water if self.min_y <= w.y <= self.max_y}


def parse(puzzle_input: str):
    """Parse input"""
    xypair_strs: list[list[str]] = [sorted(line.split(', ')) for line in puzzle_input.split('\n')]
    
    clay: list[tuple[int, ...]] = []
    for x_str, y_str in xypair_strs:
        x_str, y_str = x_str.lstrip('x='), y_str.lstrip('y=')
        if '..' in x_str:
            x_min, x_max = (int(x) for x in x_str.split('..'))
            y_min = y_max = int(y_str)
        else:
            y_min, y_max = (int(y) for y in y_str.split('..'))
            x_min = x_max = int(x_str)
        clay.append((x_min, x_max, y_min, y_max))
    return clay


def part1(data):
    """Solve part 1"""
    ground: Ground = Ground(data)
    water_source: XYtuple = (500, 0)
    ground.produce_water(water_source)
    return len(ground.all_water())


def part2(data):
    """Solve part 2"""
    ground: Ground = Ground(data)
    water_source: XYtuple = (500, 0)
    ground.produce_water(water_source)
    return len(ground.settled_water)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 57
    PART2_TEST_ANSWER = 29

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
