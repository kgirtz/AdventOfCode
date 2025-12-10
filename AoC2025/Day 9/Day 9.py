import itertools
import heapq
import typing
from collections.abc import Sequence, Iterable

from xypair import XYpair

PART1_TEST_ANSWER = 50
PART2_TEST_ANSWER = 24


XYPairHeap: typing.TypeAlias = list[tuple[int, XYpair, XYpair]]


def parse(puzzle_input: str):
    tiles: list[XYpair] = []
    for line in puzzle_input.split('\n'):
        x, y = [int(c) for c in line.split(',')]
        tiles.append(XYpair(x, y))
    return tiles


def size_of_rectangle(tile1: XYpair, tile2: XYpair) -> int:
    return (tile1.x_distance(tile2) + 1) * (tile1.y_distance(tile2) + 1)


def build_rectangle_size_heap(tiles: Iterable[XYpair]) -> XYPairHeap:
    rectangle_heap: XYPairHeap = []
    for t1, t2 in itertools.combinations(tiles, 2):
        heapq.heappush(rectangle_heap, (-size_of_rectangle(t1, t2), t1, t2))
    return rectangle_heap


def tiles_between_pairs(corner_tiles: Sequence[XYpair]) -> set[XYpair]:
    tile_borders: set[XYpair] = set()
    for t1, t2 in itertools.pairwise(list(corner_tiles) + [corner_tiles[0]]):
        if t1.x == t2.x:
            tile_borders.update(XYpair(t1.x, y) for y in range(min(t1.y, t2.y), max(t1.y, t2.y) + 1))
        else:
            tile_borders.update(XYpair(x, t1.y) for x in range(min(t1.x, t2.x), max(t1.x, t2.x) + 1))
    return tile_borders


class Floor:
    def __init__(self, red_tiles: Iterable[XYpair]) -> None:
        self.red_tiles: list[XYpair] = list(red_tiles)
        self.red_tiles.append(self.red_tiles[0])  # For cyclical pairwise iteration

        self.x_min: int = min(t.x for t in self.red_tiles)
        self.x_max: int = max(t.x for t in self.red_tiles)
        self.y_min: int = min(t.y for t in self.red_tiles)
        self.y_max: int = max(t.y for t in self.red_tiles)

        self.border_tiles: set[XYpair] = tiles_between_pairs(self.red_tiles)

    def contains(self, tile: XYpair) -> bool:
        return self.x_min <= tile.x <= self.x_max and self.y_min <= tile.y <= self.y_max

    def tiles_in_column(self, x: int) -> list[tuple[int, int]]:
        tile_intervals: list[tuple[int, int]] = []

        start: int = -1
        for y in range(self.y_min, self.y_max + 2):
            if start == -1 and (x, y) in self.border_tiles:
                start = y
            elif start != -1 and (x, y) not in self.border_tiles:
                tile_intervals.append((start, y - 1))
                start = -1

        return tile_intervals

    def tiles_in_row(self, y: int) -> list[tuple[int, int]]:
        tile_intervals: list[tuple[int, int]] = []

        start: int = -1
        for x in range(self.x_min, self.x_max + 2):
            if start == -1 and (x, y) in self.border_tiles:
                start = x
            elif start != -1 and (x, y) not in self.border_tiles:
                tile_intervals.append((start, x - 1))
                start = -1

        return tile_intervals

    def first_tile_above(self, pt: XYpair) -> XYpair | None:
        tiles_above: set[XYpair] = {t for t in self.border_tiles if t.x == pt.x and t.y < pt.y}
        if not tiles_above:
            return None
        return max(tiles_above, key=lambda t: t.y)

    def first_tile_below(self, pt: XYpair) -> XYpair | None:
        tiles_below: set[XYpair] = {t for t in self.border_tiles if t.x == pt.x and t.y > pt.y}
        if not tiles_below:
            return None
        return min(tiles_below, key=lambda t: t.y)

    def first_tile_to_left(self, pt: XYpair) -> XYpair | None:
        tiles_left: set[XYpair] = {t for t in self.border_tiles if t.y == pt.y and t.x < pt.x}
        if not tiles_left:
            return None
        return max(tiles_left)

    def first_tile_to_right(self, pt: XYpair) -> XYpair | None:
        tiles_right: set[XYpair] = {t for t in self.border_tiles if t.y == pt.y and t.x > pt.x}
        if not tiles_right:
            return None
        return min(tiles_right)


def part1(data):
    return max(size_of_rectangle(t1, t2) for t1, t2 in itertools.combinations(data, 2))


# 4634026886 is too high
def part2(data):
    floor: Floor = Floor(data)

    # Sort all possible rectangles by size
    rectangle_size_heap: XYPairHeap = build_rectangle_size_heap(data)

    while rectangle_size_heap:
        rectangle_size, t1, t2 = heapq.heappop(rectangle_size_heap)
        rectangle_size = -rectangle_size
        print(f'Checking rectangle at {t1}, {t2} (size = {rectangle_size})')

        sides: list[tuple[XYpair, XYpair]] = [(t1, XYpair(t2.x, t1.y)),
                                              (XYpair(t2.x, t1.y), t2),
                                              (t2, XYpair(t1.x, t2.y)),
                                              (XYpair(t1.x, t2.y), t1)]

        valid_sides: list[bool] = []
        for a, b in sides:
            if a.x == b.x:
                intervals: list[tuple[int, int]] = floor.tiles_in_column(a.x)
                for t1, t2 in intervals:
                    if t1 <= min(a.y, b.y) and max(a.y, b.y) <= t2:
                        valid_sides.append(True)
                        break
            else:
                intervals = floor.tiles_in_row(a.y)
                for t1, t2 in intervals:
                    if t1 <= min(a.x, b.x) and max(a.x, b.x) <= t2:
                        valid_sides.append(True)
                        break

        if len(valid_sides) == 4:
            return rectangle_size

        continue

        # Check if all red & green tiles in the rectangle
        corners: list[XYpair] = [t1, XYpair(t2.x, t1.y), t2, XYpair(t1.x, t2.y)]
        tiles_to_check: set[XYpair] = tiles_between_pairs(corners) - floor.border_tiles
        if not tiles_to_check:
            return rectangle_size

        # Explore out in straight lines to check other tiles
        top_lim = 1_000_000_000_000
        bottom_lim = 0
        left_lim = 1_000_000_000_000
        right_lim = 0
        for t in tiles_to_check:
            top_lim = min(top_lim, t.y)
            bottom_lim = max(bottom_lim, t.y)
            left_lim = min(left_lim, t.x)
            right_lim = max(right_lim, t.x)

        top_tiles = set()
        bottom_tiles = set()
        left_tiles = set()
        right_tiles = set()
        for t in tiles_to_check:
            if t.y == top_lim:
                top_tiles.add(t)
            if t.y == bottom_lim:
                bottom_tiles.add(t)
            if t.x == left_lim:
                left_tiles.add(t)
            if t.x == right_lim:
                right_tiles.add(t)

        top_left = min(top_tiles)
        top_right = max(top_tiles)
        if floor.first_tile_above(top_left) is None or floor.first_tile_to_left(top_left) is None or \
           floor.first_tile_above(top_right) is None or floor.first_tile_to_right(top_right) is None:
            continue

        bottom_left = min(bottom_tiles)
        bottom_right = max(bottom_tiles)
        if floor.first_tile_below(bottom_left) is None or floor.first_tile_to_left(bottom_left) is None or \
           floor.first_tile_below(bottom_right) is None or floor.first_tile_to_right(bottom_right) is None:
            continue

        left_top = min(left_tiles, key=lambda t: t.y)
        left_bottom = max(left_tiles, key=lambda t: t.y)
        if floor.first_tile_above(left_top) is None or floor.first_tile_to_left(left_top) is None or \
           floor.first_tile_below(left_bottom) is None or floor.first_tile_to_left(left_bottom) is None:
            continue

        right_top = min(right_tiles, key=lambda t: t.y)
        right_bottom = max(right_tiles, key=lambda t: t.y)
        if floor.first_tile_above(right_top) is None or floor.first_tile_to_right(right_top) is None or \
           floor.first_tile_below(right_bottom) is None or floor.first_tile_to_right(right_bottom) is None:
            continue

        print('Trying flood method...')

        # Flood fill to completely check other tiles
        flood: set[XYpair] = set()
        border: set[XYpair] = set(tiles_to_check)
        valid: bool = True
        while border and valid:
            tile: XYpair = border.pop()
            flood.add(tile)
            for n in tile.neighbors():
                if n in floor.border_tiles or n in flood:
                    continue
                if not floor.contains(n):
                    valid = False
                    break
                border.add(n)

        if valid:
            return rectangle_size


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
