import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    return [(line[0], int(line[2:])) for line in puzzle_input.split('\n')]


def move_head(head: Point, direction: str) -> Point:
    match direction:
        case 'U':
            return Point(head.x, head.y - 1)
        case 'D':
            return Point(head.x, head.y + 1)
        case 'L':
            return Point(head.x - 1, head.y)
        case 'R':
            return Point(head.x + 1, head.y)


def touching(p1: Point, p2: Point) -> bool:
    return abs(p1.x - p2.x) <= 1 and abs(p1.y - p2.y) <= 1


def update_follower_location(leader: Point, follower: Point, last_move_dir: str) -> tuple[Point, str]:
    if len(last_move_dir) > 1:
        if leader.x == follower.x:
            last_move_dir = last_move_dir[0]
        if leader.y == follower.y:
            last_move_dir = last_move_dir[-1]

    new_follower: Point = follower
    match last_move_dir:
        case 'U':
            new_follower = Point(leader.x, follower.y - 1)
        case 'D':
            new_follower = Point(leader.x, follower.y + 1)
        case 'L':
            new_follower = Point(follower.x - 1, leader.y)
        case 'R':
            new_follower = Point(follower.x + 1, leader.y)
        case 'UL':
            new_follower = Point(follower.x - 1, follower.y - 1)
        case 'UR':
            new_follower = Point(follower.x + 1, follower.y - 1)
        case 'DL':
            new_follower = Point(follower.x - 1, follower.y + 1)
        case 'DR':
            new_follower = Point(follower.x + 1, follower.y + 1)

    dir_moved: str = ''
    if new_follower.y == follower.y - 1:
        dir_moved += 'U'
    elif new_follower.y == follower.y + 1:
        dir_moved += 'D'

    if new_follower.x == follower.x - 1:
        dir_moved += 'L'
    elif new_follower.x == follower.x + 1:
        dir_moved += 'R'

    if not touching(leader, new_follower):
        print('INVALID MOVE')

    return new_follower, dir_moved


def move_rope(rope: list[Point], direction: str) -> None:
    rope[0] = move_head(rope[0], direction)

    for i in range(len(rope) - 1):
        leader, follower = rope[i:i + 2]
        if touching(leader, follower):
            break
        rope[i + 1], direction = update_follower_location(leader, follower, direction)


def print_rope(rope: list[Point]) -> None:
    left: int = min(min(knot.x for knot in rope), -10)
    right: int = max(max(knot.x for knot in rope), 15)
    top: int = min(min(knot.y for knot in rope), -15)
    bottom: int = max(max(knot.y for knot in rope), 5)

    area: list[list[str]] = [['.' for x in range(left, right + 1)] for y in range(top, bottom + 1)]
    area[0 - top][0 - left] = 's'

    for i, knot in enumerate(rope):
        if knot == rope[i - 1]:
            continue

        if i == 0:
            area[knot.y - top][knot.x - left] = 'H'
        else:
            area[knot.y - top][knot.x - left] = str(i)

    for row in area:
        print(''.join(row))
    print('\n')


def print_points(points: set[Point]) -> None:
    left: int = min(point.x for point in points)
    right: int = max(point.x for point in points)
    top: int = min(point.y for point in points)
    bottom: int = max(point.y for point in points)

    area: list[list[str]] = [['.' for x in range(left, right + 1)] for y in range(top, bottom + 1)]

    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if (x, y) in points:
                area[y - top][x - left] = 'X'
    area[-top][-left] = 's'

    for row in area:
        print(''.join(row))
    print('\n')


def part1(data):
    """Solve part 1"""
    rope: list[Point] = [Point(0, 0) for _ in range(2)]

    tail_points: set[Point] = {rope[-1]}

    for direction, distance in data:
        for _ in range(distance):
            move_rope(rope, direction)
            tail_points.add(rope[-1])

    return len(tail_points)


def part2(data):
    """Solve part 2"""
    rope: list[Point] = [Point(0, 0) for _ in range(10)]

    tail_points: set[Point] = {rope[-1]}

    for direction, distance in data:
        for _ in range(distance):
            move_rope(rope, direction)
            tail_points.add(rope[-1])
        # print_rope(rope)

    # print_points(tail_points)
    return len(tail_points)


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
