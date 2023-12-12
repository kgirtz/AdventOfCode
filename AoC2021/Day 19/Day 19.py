import pathlib
import sys
import os
from collections import namedtuple, deque
from typing import Optional

Point = namedtuple('Point', 'x y z')
scanners: list[Point] = []


def parse(puzzle_input):
    """Parse input"""
    scanner_data: list[str] = puzzle_input.split('\n\n')
    scanners: list[list[str]] = [scanner.split('\n') for scanner in scanner_data]
    scanner_points: list[set[Point]] = []
    for scanner in scanners:
        point_set: set[Point] = set()
        for pt in scanner[1:]:
            x, y, z = (int(c) for c in pt.split(','))
            point_set.add(Point(x, y, z))
        scanner_points.append(point_set)
    return scanner_points


def quarter_turn(pt: Point, axis: str, times: int) -> Point:
    if times == 0:
        return pt

    if axis == 'x':
        if times == 1:
            return Point(pt.x, -pt.z, pt.y)
        if times == 2:
            return Point(pt.x, -pt.y, -pt.z)
        if times == 3:
            return Point(pt.x, pt.z, -pt.y)
    if axis == 'y':
        if times == 1:
            return Point(-pt.z, pt.y, pt.x)
        if times == 2:
            return Point(-pt.x, pt.y, -pt.z)
        if times == 3:
            return Point(pt.z, pt.y, -pt.x)
    if axis == 'z':
        if times == 1:
            return Point(-pt.y, pt.x, pt.z)
        if times == 2:
            return Point(-pt.x, -pt.y, pt.z)
        if times == 3:
            return Point(pt.y, -pt.x, pt.z)


def shift(pt: Point, new_ref: Point, old_ref: Optional[Point] = None) -> Point:
    if old_ref is None:
        return Point(pt.x - new_ref.x, pt.y - new_ref.y, pt.z - new_ref.z)

    dx: int = new_ref.x - old_ref.x
    dy: int = new_ref.y - old_ref.y
    dz: int = new_ref.z - old_ref.z
    return Point(pt.x - dx, pt.y - dy, pt.z - dz)


def shell(pts: set[Point]) -> set[Point]:
    limit: int = 750
    shell_pts: set[Point] = set()
    for pt in pts:
        if abs(pt.x) > limit or abs(pt.y) > limit or abs(pt.z) > limit:
            shell_pts.add(pt)
    return shell_pts


def overlap(pts: set[Point], cloud: set[Point], cloud_shell: set[Point]) \
                                                    -> Optional[tuple[Point, Point, int, int, int]]:
    for beacon in cloud_shell:
        cloud_from_beacon: set[Point] = adjust(cloud, beacon)
        for pt in shell(pts):
            shifted_pts: set[Point] = adjust(pts, pt)
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        shifted_and_rotated: set[Point] = adjust(shifted_pts, Point(0, 0, 0), i, j, k)
                        if len(cloud_from_beacon & shifted_and_rotated) >= 12:
                            beacon_offset: Point = Point(-beacon.x, -beacon.y, -beacon.z)
                            return beacon_offset, pt, i, j, k
    return None


def adjust(pts: set[Point], translation: Point, x_rot: int = 0, y_rot: int = 0, z_rot: int = 0) -> set[Point]:
    new_pts: set[Point] = set()
    for pt in pts:
        shifted: Point = pt if translation == (0, 0, 0) else shift(pt, translation)
        shifted = quarter_turn(shifted, 'x', x_rot)
        shifted = quarter_turn(shifted, 'y', y_rot)
        shifted = quarter_turn(shifted, 'z', z_rot)
        new_pts.add(shifted)
    return new_pts


def manhattan_distance(pt1: Point, pt2: Point) -> int:
    dx: int = abs(pt1.x - pt2.x)
    dy: int = abs(pt1.y - pt2.y)
    dz: int = abs(pt1.z - pt2.z)
    return dx + dy + dz


def part1(data):
    """Solve part 1"""
    global scanners

    uncorrelated: deque[int] = deque(range(1, len(data)))
    beacons: set[Point] = data[0]
    edge_beacons: set[Point] = shell(beacons)
    scanners = [Point(0, 0, 0)]
    while uncorrelated:
        attempt: int = uncorrelated.popleft()
        new_pts: set[Point] = data[attempt]

        adjustment = overlap(new_pts, beacons, edge_beacons)
        if adjustment is not None:
            offset, match_beacon, x_rot, y_rot, z_rot = adjustment
            beacons |= adjust(adjust(new_pts, match_beacon, x_rot, y_rot, z_rot), offset)
            edge_beacons |= adjust(adjust(shell(new_pts), match_beacon, x_rot, y_rot, z_rot), offset)

            scanner: Point = Point(-match_beacon.x, -match_beacon.y, -match_beacon.z)
            scanner = adjust(adjust({scanner}, Point(0, 0, 0), x_rot, y_rot, z_rot), offset).pop()
            scanners.append(scanner)
            print(f'Scanner {attempt} added, remaining: {list(uncorrelated)}')
        else:
            uncorrelated.append(attempt)
    return len(beacons)


def part2(data):
    """Solve part 2"""
    max_dist: int = 0
    for i, s1 in enumerate(scanners):
        for s2 in scanners[i + 1:]:
            max_dist = max(max_dist, manhattan_distance(s1, s2))
    return max_dist


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
