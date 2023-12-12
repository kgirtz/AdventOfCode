import pathlib
import sys
import os
from typing import NamedTuple


class Point(NamedTuple):
    x: int = -1
    y: int = -1
    lvl: int = 0


class Portal(NamedTuple):
    name: str
    entry: Point
    target: Point


class Maze:
    def __init__(self, lines: list[str]) -> None:
        self.passages: set[Point] = set()
        self.portals: dict[Point, Point] = {}
        self.start: Point = Point()
        self.end: Point = Point()
        self.doughnut_max: Point = Point(len(lines[0]) - 3, len(lines) - 3)

        portal_descriptors: set[Portal] = set()

        # Horizontal
        for y, line in enumerate(lines[2:-2], 2):
            for x, ch in enumerate(line[1:], 1):
                if ch == '.':
                    self.passages.add(Point(x, y))
                    continue

                last_two_hor: str = line[x - 1:x + 1]
                if last_two_hor.isalpha():
                    lvl_change: int = -1 if self.is_outside_doughut(Point(x, y)) else 1

                    # Enter from left
                    if (x - 2, y, 0) in self.passages:
                        entry: Point = Point(x - 1, y, 0)
                        target: Point = Point(x - 2, y, lvl_change)
                    # Enter from right
                    else:
                        entry: Point = Point(x, y, 0)
                        target: Point = Point(x + 1, y, lvl_change)
                    portal_descriptors.add(Portal(last_two_hor, entry, target))

        # Vertical
        for x in range(2, len(lines[0]) - 2):
            for y, line in enumerate(lines[1:], 1):
                ch: str = line[x]

                last_two_vert: str = lines[y - 1][x] + ch
                if last_two_vert.isalpha():
                    lvl_change = -1 if self.is_outside_doughut(Point(x, y)) else 1

                    # Enter from above
                    if (x, y - 2, 0) in self.passages:
                        entry: Point = Point(x, y - 1, 0)
                        target: Point = Point(x, y - 2, lvl_change)
                    # Enter from below
                    else:
                        entry: Point = Point(x, y, 0)
                        target: Point = Point(x, y + 1, lvl_change)
                    portal_descriptors.add(Portal(last_two_vert, entry, target))

        # Pair portals by name
        while portal_descriptors:
            p1: Portal = portal_descriptors.pop()
            match p1.name:
                case 'AA':
                    self.start = Point(p1.target.x, p1.target.y, 0)
                case 'ZZ':
                    self.end = Point(p1.target.x, p1.target.y, 0)
                case _:
                    p2: Portal = [p for p in portal_descriptors if p.name == p1.name][0]
                    portal_descriptors.remove(p2)
                    self.portals[p1.entry] = Point(p2.target.x, p2.target.y, p1.target.lvl)
                    self.portals[p2.entry] = Point(p1.target.x, p1.target.y, p2.target.lvl)

    def neighbors(self, pos: Point) -> set[Point]:
        folded_neighbors: set[Point] = set()
        for n in (Point(pos.x - 1, pos.y),
                  Point(pos.x + 1, pos.y),
                  Point(pos.x, pos.y - 1),
                  Point(pos.x, pos.y + 1)):
            if n in self.passages:
                folded_neighbors.add(Point(n.x, n.y, pos.lvl))
            elif n in self.portals:
                dest: Point = self.portals[n]
                folded_neighbors.add(Point(dest.x, dest.y, pos.lvl + dest.lvl))

        return folded_neighbors

    def is_outside_doughut(self, pos: Point) -> bool:
        return pos.x < 2 or pos.y < 2 or pos.x > self.doughnut_max.x or pos.y > self.doughnut_max.y

    def solve(self, recursive: bool = False) -> int:
        steps: int = 0
        can_reach: set[Point] = set()
        to_check: set[Point] = {self.start}
        while to_check:
            new_to_check: set[Point] = set()
            for pt in to_check:
                if recursive:
                    new_to_check |= {n for n in self.neighbors(pt) if n.lvl >= 0}
                else:
                    new_to_check |= {Point(n.x, n.y, 0) for n in self.neighbors(pt)}

            can_reach |= to_check
            if self.end in can_reach:
                return steps

            to_check = new_to_check - can_reach
            steps += 1

        return -1


def parse(puzzle_input):
    """Parse input"""
    return Maze([line.replace('_', ' ') for line in puzzle_input.split('\n')])


def part1(data):
    """Solve part 1"""
    maze: Maze = data
    return maze.solve()


def part2(data):
    """Solve part 2"""
    maze: Maze = data
    return maze.solve(recursive=True)


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
        puzzle_input = pathlib.Path(DIR + file).read_text().replace(' ', '_').strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
