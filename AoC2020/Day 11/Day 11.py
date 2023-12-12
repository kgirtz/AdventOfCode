import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


class WaitingArea:
    def __init__(self, grid: list[str]) -> None:
        self.height: int = len(grid)
        self.width: int = len(grid[0])
        self.seats: set[Point] = set()
        for y, row in enumerate(grid):
            for x in range(len(row)):
                if grid[y][x] == 'L':
                    self.seats.add(Point(x, y))
        self.occupied: set[Point] = set()
        self.empty: set[Point] = self.seats.copy()
        self.stable: bool = False

    def neighbors(self, seat: Point) -> set[Point]:
        surrounding: set[Point] = {Point(seat.x - 1, seat.y - 1),
                                   Point(seat.x, seat.y - 1),
                                   Point(seat.x + 1, seat.y - 1),
                                   Point(seat.x - 1, seat.y),
                                   Point(seat.x + 1, seat.y),
                                   Point(seat.x - 1, seat.y + 1),
                                   Point(seat.x, seat.y + 1),
                                   Point(seat.x + 1, seat.y + 1)}
        return surrounding & self.seats

    def visible_seats(self, seat: Point) -> set[Point]:
        visible: set[Point] = set()
        x, y = seat
        while y >= 0:
            y -= 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while y < self.height:
            y += 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x >= 0:
            x -= 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x < self.width:
            x += 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x >= 0 and y >= 0:
            x -= 1
            y -= 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x < self.width and y < self.height:
            x += 1
            y += 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x >= 0 and y < self.height:
            x -= 1
            y += 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        x, y = seat
        while x < self.width and y >= 0:
            x += 1
            y -= 1
            if (x, y) in self.seats:
                visible.add(Point(x, y))
                break
        return visible

    def update(self) -> None:
        sat_down: set[Point] = {seat for seat in self.empty if len(self.neighbors(seat) & self.occupied) == 0}
        left: set[Point] = {seat for seat in self.occupied if len(self.neighbors(seat) & self.occupied) >= 4}
        if not left and not sat_down:
            self.stable = True

        self.empty = (self.empty | left) - sat_down
        self.occupied = (self.occupied | sat_down) - left

    def update_visible(self) -> None:
        sat_down: set[Point] = {seat for seat in self.empty if len(self.visible_seats(seat) & self.occupied) == 0}
        left: set[Point] = {seat for seat in self.occupied if len(self.visible_seats(seat) & self.occupied) >= 5}
        if not left and not sat_down:
            self.stable = True

        self.empty = (self.empty | left) - sat_down
        self.occupied = (self.occupied | sat_down) - left


def part1(data):
    """Solve part 1"""
    area: WaitingArea = WaitingArea(data)
    while not area.stable:
        area.update()
    return len(area.occupied)


def part2(data):
    """Solve part 2"""
    area: WaitingArea = WaitingArea(data)
    while not area.stable:
        area.update_visible()
    return len(area.occupied)


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
