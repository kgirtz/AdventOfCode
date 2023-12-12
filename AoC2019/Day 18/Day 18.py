import pathlib
import sys
import os
from typing import NamedTuple, Iterable, Union


class Point(NamedTuple):
    x: int = -1
    y: int = -1


class AreaScan:
    def __init__(self, entrance: Point, passages: Iterable[Point], keys: dict[str, Point], doors: dict[str, Point]) -> None:
        self.entrance: Point = entrance
        self.passages: frozenset[Point] = frozenset(passages)
        self.keys: dict[str, Point] = dict(keys)
        self.doors: dict[str, Point] = dict(doors)
        self.key_locations: dict[Point, str] = {pt: k for k, pt in self.keys.items()}
        self.door_locations: dict[Point, str] = {pt: k for k, pt in self.doors.items()}
        self.reachable_keys: dict[tuple[Point, frozenset[str]], dict[str, int]] = {}
        self.min_steps: dict[tuple[frozenset[Point], frozenset[str]], Union[int, tuple[int, list[str]]]] = {}
        self.passage_neighbors: dict[Point, frozenset[Point]] = {}

    def print_state(self, positions: Iterable[Point], keys_collected: Iterable[str]) -> None:
        positions = set(positions)
        keys_collected = set(keys_collected)

        x_max: int = max(pt.x for pt in self.passages) + 1
        y_max: int = max(pt.y for pt in self.passages) + 1

        print()
        print('#' * (x_max + 1))

        for y in range(1, y_max):
            line: str = '#'
            for x in range(1, x_max):
                if (x, y) in positions:
                    line += '@'
                elif (x, y) in self.key_locations.keys() - keys_collected:
                    line += self.key_locations[Point(x, y)]
                elif (x, y) in self.door_locations.keys() and self.door_locations[Point(x, y)] not in keys_collected:
                    line += self.door_locations[Point(x, y)].upper()
                elif (x, y) in self.passages:
                    line += '.'
                else:
                    line += '#'
            print(line + '#')

        print('#' * (x_max + 1))

    def neighbors(self, pos: Point) -> set[Point]:
        # Memoize
        params: Point = pos
        if params in self.passage_neighbors:
            return set(self.passage_neighbors[params])

        n: set[Point] = {Point(pos.x - 1, pos.y),
                         Point(pos.x + 1, pos.y),
                         Point(pos.x, pos.y - 1),
                         Point(pos.x, pos.y + 1)} & self.passages

        # Memoize
        self.passage_neighbors[params] = frozenset(n)
        return n

    def all_reachable_keys(self, cur_pos: Point, keys_collected: set[str]) -> dict[str, int]:
        # Memoize
        params: tuple[Point, frozenset[str]] = (cur_pos, frozenset(keys_collected))
        if params in self.reachable_keys:
            return self.reachable_keys[params]

        locked_doors: set[Point] = {pt for d, pt in self.doors.items() if d.lower() not in keys_collected}
        keys_to_find: set[str] = self.keys.keys() - keys_collected

        key_distances: dict[str, int] = {}

        steps: int = 0
        can_reach: set[Point] = set()
        to_check: set[Point] = {cur_pos}
        while keys_to_find and to_check:
            new_to_check: set[Point] = set()
            for pt in to_check:
                new_to_check |= self.neighbors(pt)

            can_reach |= to_check
            to_check = new_to_check - can_reach - locked_doors
            steps += 1

            for pt in to_check.copy():
                key: str = self.key_locations.get(pt, None)
                if key in keys_to_find:
                    key_distances[key] = steps
                    keys_to_find.remove(key)
                    to_check.remove(self.keys[key])

        # Memoize
        self.reachable_keys[params] = key_distances
        return key_distances

    def collect_all_keys(self, cur_pos: Point, keys_collected: set[str] = None) -> int:
        if keys_collected is None:
            keys_collected = set()
        if keys_collected == self.keys.keys():
            return 0

        # Memoize
        params: tuple[frozenset[Point], frozenset[str]] = (frozenset([cur_pos]), frozenset(keys_collected))
        if params in self.min_steps:
            return self.min_steps[params]

        # Decide which key to collect next
        steps: int = -1
        for key, dist in self.all_reachable_keys(cur_pos, keys_collected).items():
            sub_steps: int = self.collect_all_keys(self.keys[key], keys_collected | {key}) + dist
            steps = min(sub_steps, steps) if steps >= 0 else sub_steps

        # Memoize
        self.min_steps[params] = steps
        return steps

    def collect_all_keys_with_robots(self, positions: set[Point], keys_collected: set[str] = None) -> tuple[int, list[str]]:
        if keys_collected is None:
            keys_collected = set()
        if keys_collected == self.keys.keys():
            return 0, []

        # Memoize
        params: tuple[frozenset[Point], frozenset[str]] = (frozenset(positions), frozenset(keys_collected))
        if params in self.min_steps:
            return self.min_steps[params]

        # Decide which key to collect next
        steps: int = -1
        optimal_key_order: list[str] = []
        for pos in positions:
            for key, dist in self.all_reachable_keys(pos, keys_collected).items():
                sub_steps, key_order = self.collect_all_keys_with_robots((positions - {pos}) | {self.keys[key]}, keys_collected | {key})
                sub_steps += dist
                if steps < 0 or sub_steps < steps:
                    steps = sub_steps
                    optimal_key_order = [key] + key_order

        # Memoize
        self.min_steps[params] = (steps, optimal_key_order)
        return steps, optimal_key_order


def parse(puzzle_input):
    """Parse input"""
    passages: set[Point] = set()
    keys: dict[str, Point] = {}
    doors: dict[str, Point] = {}
    entrance: Point = Point(-1, -1)

    for y, line in enumerate(puzzle_input.split('\n')):
        for x, ch in enumerate(line):
            if ch == '#':
                continue

            pos: Point = Point(x, y)
            passages.add(pos)

            if ch == '@':
                entrance = pos
            elif ch.islower():
                keys[ch] = pos
            elif ch.isupper():
                doors[ch] = pos

    return entrance, passages, keys, doors


def part1(data):
    """Solve part 1"""
    entrance, passages, keys, doors = data
    area: AreaScan = AreaScan(*data)
    return area.collect_all_keys(entrance)


def part2(data):
    """Solve part 2"""
    entrance, passages, keys, doors = data
    area: AreaScan = AreaScan(*data)

    # Modify starting configuration for robots
    area.passages -= area.neighbors(entrance) | {entrance}
    starting_positions: set[Point] = {Point(entrance.x - 1, entrance.y - 1),
                                      Point(entrance.x - 1, entrance.y + 1),
                                      Point(entrance.x + 1, entrance.y - 1),
                                      Point(entrance.x + 1, entrance.y + 1)}

    return area.collect_all_keys_with_robots(starting_positions)


def solve1(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    return solution1


def solve2(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution2, order = part2(data)
    return solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    for file, result in zip(('example.txt', 'example2.txt', 'example3.txt', 'example4.txt',), (86, 132, 136, 81)):
        print(f"{file}:", end='')
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        assert solve1(puzzle_input) == result
        print("PASS")
    print()

    for file, result in zip(('example5.txt', 'example6.txt', 'example7.txt', 'example8.txt',), (8, 24, 32, 72)):
        print(f"{file}:", end='')
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        assert solve2(puzzle_input) == result
        print("PASS")
    print()

    file = 'input.txt'
    print(f"{file}:")
    puzzle_input = pathlib.Path(DIR + file).read_text().strip()
    print(solve2(puzzle_input))
    print()
