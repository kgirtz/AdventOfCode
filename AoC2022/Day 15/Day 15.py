import pathlib
import sys
import os
import re
from collections import namedtuple
from typing import Optional
import cProfile

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    sensors: list[tuple[Point, Point, int]] = []
    pattern: str = r'x=(-?\d+), y=(-?\d+)'
    for line in puzzle_input.split('\n'):
        xy_pairs: list[tuple[str, str]] = re.findall(pattern, line)
        sensor: Point = Point(*(int(coord) for coord in xy_pairs[0]))
        beacon: Point = Point(*(int(coord) for coord in xy_pairs[1]))
        d: int = manhattan_distance(sensor, beacon)
        sensors.append((sensor, beacon, d))

    return sensors


def manhattan_distance(pt1: Point, pt2: Point) -> int:
    return abs(pt1.x - pt2.x) + abs(pt1.y - pt2.y)


def get_horizontal_line_intercepts(sensor: Point, radius: int, y: int) -> Optional[tuple[int, int]]:
    delta_y: int = abs(sensor.y - y)
    if delta_y > radius:
        return None

    left: int = sensor.x - (radius - delta_y)
    right: int = sensor.x + (radius - delta_y)

    return left, right


def merge_segments(segments: list[tuple[int, int]]) -> None:
    segments.sort()

    i: int = 0
    while i != len(segments) - 1:
        cur_seg: tuple[int, int] = segments[i]
        next_seg: tuple[int, int] = segments[i + 1]
        if cur_seg[1] >= next_seg[0]:
            segments[i] = (cur_seg[0], max(cur_seg[1], next_seg[1]))
            segments.remove(next_seg)
            continue
        i += 1


def beacon_on_horizontal_segment(sensors: list[tuple[Point, Point, int]], y: int, x: tuple[int, int]) -> int:
    segments: list[tuple[int, int]] = []
    finished_sensors: list[tuple[Point, Point, int]] = []
    for sensor, beacon, d in sensors:
        intercepts: Optional[tuple[int, int]] = get_horizontal_line_intercepts(sensor, d, y)
        if intercepts:
            if intercepts[1] < x[0] or intercepts[0] > x[1]:
                continue
            intercepts = (max(intercepts[0], x[0]), min(intercepts[1], x[1]))
            segments.append(intercepts)
        elif sensor.y < y:
            finished_sensors.append((sensor, beacon, d))

    for s in finished_sensors:
        sensors.remove(s)

    segments.sort()

    distress_signal: int = x[0]
    for left, right in segments:
        if distress_signal < left:
            return distress_signal
        if distress_signal <= right:
            distress_signal = right + 1

    return distress_signal


def tuning_frequency(beacon: Point) -> int:
    return 4000000 * beacon.x + beacon.y


def part1(data):
    """Solve part 1"""
    y: int = 2000000

    segments: list[tuple[int, int]] = []
    for sensor, beacon, d in data:
        intercepts: Optional[tuple[int, int]] = get_horizontal_line_intercepts(sensor, d, y)
        if intercepts:
            segments.append(intercepts)

    merge_segments(segments)

    non_beacon_points: int = 0
    for left, right in segments:
        non_beacon_points += right - left + 1

    intercept_beacons: set[Point] = {beacon for _, beacon, _ in data if beacon.y == y}

    return non_beacon_points - len(intercept_beacons)


def part2(data):
    """Solve part 2"""
    x_min, y_min = 0, 0
    x_max, y_max = 4000000, 4000000

    for y in range(y_min, y_max + 1):
        x: int = beacon_on_horizontal_segment(data, y, (x_min, x_max))
        if x <= x_max:
            return tuning_frequency(Point(x, y))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt', ):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
