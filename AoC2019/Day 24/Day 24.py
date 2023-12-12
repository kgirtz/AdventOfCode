import pathlib
import sys
import os
from typing import NamedTuple, Optional
from collections.abc import Iterable


class Point(NamedTuple):
    x: int
    y: int


class Grid:
    def __init__(self, side_len: int, lvl: int = 0) -> None:
        self.side_len: int = side_len
        self.bugs: set[Point] = set()
        self.outer_grid: Optional[Grid] = None
        self.inner_grid: Optional[Grid] = None
        self.center: Point = Point(side_len // 2, side_len // 2)
        self.lvl: int = lvl

    def set_bugs(self, bugs: Iterable[Point]) -> None:
        self.bugs = {bug for bug in bugs if self.in_grid(bug)}

    def create_inner_grid(self) -> None:
        if self.inner_grid is None:
            self.inner_grid = Grid(self.side_len, self.lvl + 1)
            self.inner_grid.outer_grid = self

    def create_outer_grid(self) -> None:
        if self.outer_grid is None:
            self.outer_grid = Grid(self.side_len, self.lvl - 1)
            self.outer_grid.inner_grid = self

    def in_grid(self, pt: Point) -> bool:
        return 0 <= pt.x < self.side_len and 0 <= pt.y < self.side_len

    def on_left_edge(self, pt: Point) -> bool:
        return pt.x == 0 and self.in_grid(pt)

    def on_right_edge(self, pt: Point) -> bool:
        return pt.x == self.side_len - 1 and self.in_grid(pt)

    def on_top_edge(self, pt: Point) -> bool:
        return pt.y == 0 and self.in_grid(pt)

    def on_bottom_edge(self, pt: Point) -> bool:
        return pt.y == self.side_len - 1 and self.in_grid(pt)

    def left_of_center(self, pt: Point) -> bool:
        return pt == (self.center.x - 1, self.center.y)

    def right_of_center(self, pt: Point) -> bool:
        return pt == (self.center.x + 1, self.center.y)

    def above_center(self, pt: Point) -> bool:
        return pt == (self.center.x, self.center.y - 1)

    def below_center(self, pt: Point) -> bool:
        return pt == (self.center.x, self.center.y + 1)

    def bug_left_of_center(self) -> bool:
        return Point(self.center.x - 1, self.center.y) in self.bugs

    def bug_right_of_center(self) -> bool:
        return Point(self.center.x + 1, self.center.y) in self.bugs

    def bug_above_center(self) -> bool:
        return Point(self.center.x, self.center.y - 1) in self.bugs

    def bug_below_center(self) -> bool:
        return Point(self.center.x, self.center.y + 1) in self.bugs

    def num_bugs_on_left_edge(self) -> int:
        return len({Point(0, y) for y in range(self.side_len)} & self.bugs)

    def num_bugs_on_right_edge(self) -> int:
        return len({Point(self.side_len - 1, y) for y in range(self.side_len)} & self.bugs)

    def num_bugs_on_top_edge(self) -> int:
        return len({Point(x, 0) for x in range(self.side_len)} & self.bugs)

    def num_bugs_on_bottom_edge(self) -> int:
        return len({Point(x, self.side_len - 1) for x in range(self.side_len)} & self.bugs)

    def has_bug_on_outside_edge(self) -> bool:
        return self.num_bugs_on_left_edge() > 0 or self.num_bugs_on_right_edge() > 0 or \
               self.num_bugs_on_top_edge() > 0 or self.num_bugs_on_bottom_edge() > 0

    def has_bug_around_center(self) -> bool:
        return len({Point(self.center.x - 1, self.center.y),
                    Point(self.center.x + 1, self.center.y),
                    Point(self.center.x, self.center.y - 1),
                    Point(self.center.x, self.center.y + 1)} & self.bugs) != 0

    def num_neighbors(self, pt: Point) -> int:
        neighbors: set[Point] = {pt for pt in (Point(pt.x - 1, pt.y),
                                               Point(pt.x + 1, pt.y),
                                               Point(pt.x, pt.y - 1),
                                               Point(pt.x, pt.y + 1))
                                 if self.in_grid(pt)}

        # Account for inner grid
        num_inner_neighbors: int = 0
        if self.inner_grid is not None:
            neighbors.discard(self.center)

            if self.left_of_center(pt):
                num_inner_neighbors += self.inner_grid.num_bugs_on_left_edge()
            elif self.right_of_center(pt):
                num_inner_neighbors += self.inner_grid.num_bugs_on_right_edge()
            elif self.above_center(pt):
                num_inner_neighbors += self.inner_grid.num_bugs_on_top_edge()
            elif self.below_center(pt):
                num_inner_neighbors += self.inner_grid.num_bugs_on_bottom_edge()

        # Account for outer grid
        num_outer_neighbors: int = 0
        if self.outer_grid is not None:
            if self.on_left_edge(pt) and self.outer_grid.bug_left_of_center():
                num_outer_neighbors += 1
            if self.on_right_edge(pt) and self.outer_grid.bug_right_of_center():
                num_outer_neighbors += 1
            if self.on_top_edge(pt) and self.outer_grid.bug_above_center():
                num_outer_neighbors += 1
            if self.on_bottom_edge(pt) and self.outer_grid.bug_below_center():
                num_outer_neighbors += 1

        return len(neighbors & self.bugs) + num_inner_neighbors + num_outer_neighbors

    def update_bugs(self, folded: bool = False) -> None:
        new_bugs: set[Point] = set()
        for y in range(self.side_len):
            for x in range(self.side_len):
                cur_pt: Point = Point(x, y)
                if folded and cur_pt == self.center:
                    continue

                num_adjacent_bugs: int = self.num_neighbors(cur_pt)
                if num_adjacent_bugs == 1 or (num_adjacent_bugs == 2 and cur_pt not in self.bugs):
                    new_bugs.add(cur_pt)

        if folded:
            # Recurse inward
            if self.lvl >= 0:
                if self.inner_grid is None and self.has_bug_around_center():
                    self.create_inner_grid()
                if self.inner_grid is not None:
                    self.inner_grid.update_bugs(folded)

            # Recurse outward
            if self.lvl <= 0:
                if self.outer_grid is None and self.has_bug_on_outside_edge():
                    self.create_outer_grid()
                if self.outer_grid is not None:
                    self.outer_grid.update_bugs(folded)

        self.bugs = new_bugs

    def find_first_repeated_state(self) -> None:
        states_seen: set[frozenset[Point]] = set()
        cur_state: frozenset[Point] = frozenset(self.bugs)
        while cur_state not in states_seen:
            states_seen.add(cur_state)
            self.update_bugs()
            cur_state = frozenset(self.bugs)

    def biodiversity_rating(self) -> int:
        return sum(pow(2, bug.y * self.side_len + bug.x) for bug in self.bugs)

    def bug_count(self) -> int:
        # Recurse inward
        inner_bugs: int = 0
        if self.lvl >= 0 and self.inner_grid is not None:
            inner_bugs += self.inner_grid.bug_count()

        # Recurse outward
        outer_bugs: int = 0
        if self.lvl <= 0 and self.outer_grid is not None:
            outer_bugs += self.outer_grid.bug_count()

        return len(self.bugs) + inner_bugs + outer_bugs


def parse(puzzle_input):
    """Parse input"""
    bugs: set[Point] = set()
    for y, line in enumerate(puzzle_input.split('\n')):
        for x, ch in enumerate(line):
            if ch == '#':
                bugs.add(Point(x, y))
    return bugs


def part1(data):
    """Solve part 1"""
    grid: Grid = Grid(5)
    grid.set_bugs(data)
    grid.find_first_repeated_state()
    return grid.biodiversity_rating()


def part2(data):
    """Solve part 2"""
    grid: Grid = Grid(5)
    grid.set_bugs(data)
    for _ in range(200):
        grid.update_bugs(folded=True)
    return grid.bug_count()


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
