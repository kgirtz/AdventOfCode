import itertools
import heapq
from collections.abc import Sequence

from xypair import XYpair

PART1_TEST_ANSWER = 50
PART2_TEST_ANSWER = 24


def parse(puzzle_input: str):
    tiles: list[XYpair] = []
    for line in puzzle_input.split('\n'):
        x, y = [int(c) for c in line.split(',')]
        tiles.append(XYpair(x, y))
    return tiles


def size_of_rectangle(corner1: XYpair, corner2: XYpair) -> int:
    return (corner1.x_distance(corner2) + 1) * (corner1.y_distance(corner2) + 1)


class Floor:
    def __init__(self, red_tiles: Sequence[XYpair]) -> None:
        self.red_tiles: list[XYpair] = list(red_tiles)

        # Organize corner tile pairs for quick access
        self.vertical_segments: list[tuple[XYpair, XYpair, bool]] = []
        self.horizontal_segments: list[tuple[XYpair, XYpair, bool]] = []
        for i, t1 in enumerate(self.red_tiles):
            t0: XYpair = self.red_tiles[(i - 1) % len(self.red_tiles)]
            t2: XYpair = self.red_tiles[(i + 1) % len(self.red_tiles)]
            t3: XYpair = self.red_tiles[(i + 2) % len(self.red_tiles)]

            # Vertical
            if t1.x == t2.x:
                is_s_curve: bool = (t1.x - t0.x) * (t1.x - t3.x) < 0
                if t1.y > t2.y:
                    t1, t2 = t2, t1
                self.vertical_segments.append((t1, t2, is_s_curve))

            # Horizontal
            else:
                is_s_curve = (t1.y - t0.y) * (t1.y - t3.y) < 0
                if t1.x > t2.x:
                    t1, t2 = t2, t1
                self.horizontal_segments.append((t1, t2, is_s_curve))

        self.vertical_segments.sort()
        self.horizontal_segments.sort()

    def tile_intervals_in_column(self, x: int) -> list[tuple[int, int]]:
        intersectors: list[tuple[int, int, bool]] = []

        for t1, t2, is_s_curve in self.vertical_segments:
            if t1.x == x:
                intersectors.append((t1.y, t2.y, is_s_curve))
            elif t1.x > x:
                break

        for t1, t2, is_s_curve in self.horizontal_segments:
            if t1.x < x < t2.x:
                intersectors.append((t1.y, t1.y, is_s_curve))
            elif t1.x > x:
                break

        intersectors.sort()

        # Determine intervals of tiles using corner intersections
        tile_intervals: list[tuple[int, int]] = []

        start: int = -1
        for y1, y2, is_s_curve in intersectors:
            # Intersection or S-curve must start or end a line of tiles
            if y1 == y2 or is_s_curve:
                if start == -1:
                    start = y1
                else:
                    tile_intervals.append((start, y2))
                    start = -1

            # Overlap is isolated or sub interval if not an S-curve
            elif start == -1:
                tile_intervals.append((y1, y2))

        return tile_intervals

    def tile_intervals_in_row(self, y: int) -> list[tuple[int, int]]:
        intersectors: list[tuple[int, int, bool]] = []

        for t1, t2, is_s_curve in self.horizontal_segments:
            if t1.y == y:
                intersectors.append((t1.x, t2.x, is_s_curve))

        for t1, t2, is_s_curve in self.vertical_segments:
            if t1.y < y < t2.y:
                intersectors.append((t1.x, t1.x, is_s_curve))

        intersectors.sort()

        # Determine intervals of tiles using corner intersections
        tile_intervals: list[tuple[int, int]] = []

        start: int = -1
        for x1, x2, is_s_curve in intersectors:
            # Intersection or S-curve must start or end a line of tiles
            if x1 == x2 or is_s_curve:
                if start == -1:
                    start = x1
                else:
                    tile_intervals.append((start, x2))
                    start = -1

            # Overlap is isolated or sub interval if not an S-curve
            elif start == -1:
                tile_intervals.append((x1, x2))

        return tile_intervals


def part1(data):
    return max(size_of_rectangle(t1, t2) for t1, t2 in itertools.combinations(data, 2))


def part2(data):
    floor: Floor = Floor(data)

    # Heap sort rectangles by size
    rectangles: list[tuple[int, XYpair, XYpair]] = []
    for t1, t2 in itertools.combinations(data, 2):
        heapq.heappush(rectangles, (-size_of_rectangle(t1, t2), t1, t2))

    while rectangles:
        rectangle_size, t1, t2 = heapq.heappop(rectangles)

        t3: XYpair = XYpair(t2.x, t1.y)
        t4: XYpair = XYpair(t1.x, t2.y)
        sides: list[tuple[XYpair, XYpair]] = [(t1, t3),
                                              (t3, t2),
                                              (t2, t4),
                                              (t4, t1)]

        valid_rectangle: bool = True
        for a, b in sides:
            valid_side: bool = False

            if a.x == b.x:
                intervals: list[tuple[int, int]] = floor.tile_intervals_in_column(a.x)
                for y1, y2 in intervals:
                    if y1 <= min(a.y, b.y) and max(a.y, b.y) <= y2:
                        valid_side = True
                        break
            else:
                intervals = floor.tile_intervals_in_row(a.y)
                for x1, x2 in intervals:
                    if x1 <= min(a.x, b.x) and max(a.x, b.x) <= x2:
                        valid_side = True
                        break

            if not valid_side:
                valid_rectangle = False
                break

        if valid_rectangle:
            return -rectangle_size


# ------------- DO NOT MODIFY BELOW THIS LINE ------------- #


import pathlib


def get_puzzle_input(file: pathlib.Path) -> str:
    if not file.exists():
        return ''
    return file.read_text().strip('\n').replace('\t', ' ' * 4)


def execute(func, puzzle_input: str) -> (..., int):
    import time

    start: int = time.perf_counter_ns()
    result = func(parse(puzzle_input))
    execution_time_us: int = (time.perf_counter_ns() - start) // 1000
    return result, execution_time_us


def timestamp(execution_time_us: int) -> str:
    stamp: str = f'{round(execution_time_us / 1000000, 3)} s'
    if execution_time_us < 1000000:
        stamp = f'{round(execution_time_us / 1000, 3)} ms'
    return f'\t[{stamp}]'


def test(part_num: int, directory: str) -> None:
    if part_num == 1:
        func = part1
        answer = PART1_TEST_ANSWER
    else:
        func = part2
        answer = PART2_TEST_ANSWER

    prefix: str = f'PART {part_num} TEST: '
    if answer is None:
        print(prefix + 'skipped')
        return

    file: pathlib.Path = pathlib.Path(directory, f'part{part_num}_test.txt')
    if not file.exists():
        file = pathlib.Path(directory, 'test.txt')

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    result = 'PASS' if result == answer else 'FAIL'
    print(prefix + result + timestamp(duration))


def solve(part_num: int, directory: str) -> None:
    func = part1 if part_num == 1 else part2
    prefix: str = f'PART {part_num}: '

    file: pathlib.Path = pathlib.Path(directory, 'input.txt')
    if not file.exists():
        # Download file?
        ...

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    suffix: str = '' if result is None else timestamp(duration)
    print(prefix + str(result) + suffix)


if __name__ == '__main__':
    import os

    working_directory: str = os.path.dirname(__file__)

    test(1, working_directory)
    test(2, working_directory)
    print()
    solve(1, working_directory)
    solve(2, working_directory)
