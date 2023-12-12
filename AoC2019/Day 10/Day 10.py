import pathlib
import sys
import os
from typing import Optional
from collections import namedtuple
from math import gcd

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def reduce(a: int, b: int) -> tuple[int, int]:
    common: int = gcd(a, b)
    return a // common, b // common


class AsteroidMap:
    def __init__(self, asteroids: list[str]) -> None:
        self.x_max: int = len(asteroids[0]) - 1
        self.y_max: int = len(asteroids) - 1
        self.asteroids: set[Point] = set()
        for y, row in enumerate(asteroids):
            for x, pixel in enumerate(row):
                if pixel == '#':
                    self.asteroids.add(Point(x, y))

    def on_map(self, pt: Point) -> bool:
        return 0 <= pt.x <= self.x_max and 0 <= pt.y <= self.y_max

    def asteroids_visible_from(self, pt: Point) -> int:
        visible: int = 0
        searchable: set[Point] = self.asteroids.copy() - {pt}

        while searchable:
            visible += 1
            asteroid: Point = searchable.pop()
            del_x, del_y = reduce(asteroid.x - pt.x, asteroid.y - pt.y)
            trajectory: Point = Point(pt.x + del_x, pt.y + del_y)
            while self.on_map(trajectory):
                searchable.discard(trajectory)
                trajectory = Point(trajectory.x + del_x, trajectory.y + del_y)

        return visible

    def station(self) -> tuple[Point, int]:
        best_station: Point = Point(0, 0)
        most_visible: int = 0
        for asteroid in self.asteroids:
            visible: int = self.asteroids_visible_from(asteroid)
            if visible > most_visible:
                most_visible = visible
                best_station = asteroid
        return best_station, most_visible

    def visible_trajectories(self, pt: Point) -> set[Point]:
        searchable: set[Point] = self.asteroids.copy() - {pt}
        trajectories: set[Point] = set()
        while searchable:
            asteroid: Point = searchable.pop()
            del_x, del_y = reduce(asteroid.x - pt.x, asteroid.y - pt.y)
            trajectories.add(Point(del_x, del_y))

            trajectory: Point = Point(pt.x + del_x, pt.y + del_y)
            while self.on_map(trajectory):
                searchable.discard(trajectory)
                trajectory = Point(trajectory.x + del_x, trajectory.y + del_y)

        return trajectories

    def vaporize(self, pt: Point, trajectory: Point) -> Optional[Point]:
        target: Point = Point(pt.x + trajectory.x, pt.y + trajectory.y)
        while self.on_map(target) and target not in self.asteroids:
            target = Point(target.x + trajectory.x, target.y + trajectory.y)

        if target in self.asteroids:
            self.asteroids.remove(target)
            return target
        else:
            return None


def clockwise(trajectories: set[Point]) -> list[Point]:
    q14: list[Point] = [t for t in trajectories if t.x > 0]
    q23: list[Point] = [t for t in trajectories if t.x < 0]

    q14.sort(key=lambda traj: traj.y / traj.x)
    q23.sort(key=lambda traj: traj.y / traj.x)

    y_pos: list[Point] = [t for t in trajectories if t.x == 0 and t.y > 0]
    y_neg: list[Point] = [t for t in trajectories if t.x == 0 and t.y < 0]

    return y_neg + q14 + y_pos + q23


def part1(data):
    """Solve part 1"""
    am: AsteroidMap = AsteroidMap(data)
    _, visible = am.station()
    return visible


def part2(data):
    """Solve part 2"""
    am: AsteroidMap = AsteroidMap(data)
    station, _ = am.station()
    trajectories: list[Point] = clockwise(am.visible_trajectories(station))

    cur: int = trajectories.index(Point(0, -1))
    vaporized: int = 0
    while am.asteroids - {station}:
        destroyed: Optional[Point] = am.vaporize(station, trajectories[cur])
        if destroyed is not None:
            vaporized += 1
            if vaporized == 200:
                return 100 * destroyed.x + destroyed.y

        cur = (cur + 1) % len(trajectories)


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
