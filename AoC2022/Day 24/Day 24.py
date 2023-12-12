import pathlib
import sys
import os
from collections import namedtuple, defaultdict

Point = namedtuple('Point', 'x y')

BlizzardDict = dict[Point, set[str]]


def parse(puzzle_input):
    """Parse input"""
    lines: list[str] = [line.strip('#') for line in puzzle_input.split('\n')[1:-1]]
    valley: Valley = Valley(lines)

    blizzards: BlizzardDict = defaultdict(set)
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            if pos != '.':
                blizzards[Point(x, y)].add(pos)

    return valley, dict(blizzards)


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


class Valley:
    def __init__(self, scan: list[str]) -> None:
        self.width: int = len(scan[0])
        self.height: int = len(scan)
        self.start: Point = Point(0, -1)
        self.end: Point = Point(self.width - 1, self.height)

    def update_blizzards(self, blizzards: BlizzardDict) -> BlizzardDict:
        new_blizzards: BlizzardDict = defaultdict(set)
        for (x, y), directions in blizzards.items():
            for direction in directions:
                match direction:
                    case '<':
                        new_blizzards[Point((x - 1) % self.width, y)].add(direction)
                    case '>':
                        new_blizzards[Point((x + 1) % self.width, y)].add(direction)
                    case '^':
                        new_blizzards[Point(x, (y - 1) % self.height)].add(direction)
                    case 'v':
                        new_blizzards[Point(x, (y + 1) % self.height)].add(direction)

        return new_blizzards

    def neighbors(self, pt: Point) -> set[Point]:
        if pt == self.start:
            return {Point(self.start.x, self.start.y + 1)}
        if pt == self.end:
            return {Point(self.end.x, self.end.y - 1)}

        n: set[Point] = set()
        if pt.x > 0:
            n.add(Point(pt.x - 1, pt.y))
        if pt.x < self.width - 1:
            n.add(Point(pt.x + 1, pt.y))
        if pt.y > 0 or pt == (self.start.x, self.start.y + 1):
            n.add(Point(pt.x, pt.y - 1))
        if pt.y < self.height - 1 or pt == (self.end.x, self.end.y - 1):
            n.add(Point(pt.x, pt.y + 1))
        return n


def min_travel_time(start: Point, end: Point, valley: Valley, blizzards: BlizzardDict) -> tuple[int, BlizzardDict]:
    minutes_elapsed: int = 0
    states: set[Point] = {start}
    while states:
        minutes_elapsed += 1
        blizzards = valley.update_blizzards(blizzards)

        # All moves/holds without blizzards
        new_states: set[Point] = set(states)
        for pt in states:
            new_states |= valley.neighbors(pt)
        new_states -= blizzards.keys()

        if end in new_states:
            return minutes_elapsed, blizzards

        states = new_states
    return -1, blizzards


def part1(data):
    """Solve part 1"""
    valley, blizzards = data
    min_time, _ = min_travel_time(valley.start, valley.end, valley, blizzards)

    return min_time


def part2(data):
    """Solve part 2"""
    valley, blizzards = data
    first_trip, blizzards = min_travel_time(valley.start, valley.end, valley, blizzards)
    second_trip, blizzards = min_travel_time(valley.end, valley.start, valley, blizzards)
    third_trip, blizzards = min_travel_time(valley.start, valley.end, valley, blizzards)

    return first_trip + second_trip + third_trip


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
