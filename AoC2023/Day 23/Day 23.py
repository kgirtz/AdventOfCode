import pathlib
import sys
import os
import functools
from point import Point
from typing import Sequence, Iterable
from collections import defaultdict


class TrailMap:
    def __init__(self, trail_map: Sequence[str]) -> None:
        self.paths: dict[Point, str] = {}
        for y, line in enumerate(trail_map):
            for x, ch in enumerate(line):
                if ch != '#':
                    self.paths[Point(x, y)] = ch

        self.weighted_edges: dict[Point, dict[Point, int]] = self.make_graph()

    def melt_ice(self) -> None:
        self.paths = {path: '.' for path in self.paths}
        self.weighted_edges = self.make_graph()

    def walkable(self, cur_pos: Point, target: Point) -> bool:
        if target.is_above(cur_pos):
            return self.paths[target] != 'v'
        if target.is_below(cur_pos):
            return self.paths[target] != '^'
        if target.is_left_of(cur_pos):
            return self.paths[target] != '>'
        if target.is_right_of(cur_pos):
            return self.paths[target] != '<'

    def make_graph(self) -> dict[Point, dict[Point, int]]:
        outgoing: dict[Point, set[Point]] = defaultdict(set)
        incoming: dict[Point, set[Point]] = defaultdict(set)
        for path, path_type in self.paths.items():
            match path_type:
                case '^':
                    above: Point = path.above()
                    if self.paths.get(above, '#') not in ('v', '#'):
                        outgoing[path].add(above)
                        incoming[above].add(path)
                case 'v':
                    below: Point = path.below()
                    if self.paths.get(below, '#') not in ('^', '#'):
                        outgoing[path].add(below)
                        incoming[below].add(path)
                case '<':
                    left: Point = path.left()
                    if self.paths.get(left, '#') not in ('>', '#'):
                        outgoing[path].add(left)
                        incoming[left].add(path)
                case '>':
                    right: Point = path.right()
                    if self.paths.get(right, '#') not in ('<', '#'):
                        outgoing[path].add(right)
                        incoming[right].add(path)
                case _:
                    for n in path.neighbors():
                        if n in self.paths and self.walkable(path, n):
                            outgoing[path].add(n)
                            incoming[n].add(path)

        sorted_paths: list[Point] = sorted(self.paths.keys(), key=lambda pt: pt.y)
        start: Point = sorted_paths[0]
        end: Point = sorted_paths[-1]

        graph: dict[Point, dict[Point, int]] = {start: {}, end: {}}
        graph.update({p: {} for p in self.paths if len(outgoing[p]) >= 3})
        graph.update({p: {} for p in self.paths if len(outgoing[p]) == 2 and incoming[p] - outgoing[p]})

        for node, edges in graph.items():
            for next_step in outgoing[node]:
                cur_pos: Point = node
                num_steps: int = 1
                next_steps: set[Point] = outgoing[next_step] - {cur_pos}
                while len(next_steps) == 1:
                    num_steps += 1
                    cur_pos = next_step
                    next_step = next_steps.pop()
                    next_steps = outgoing[next_step] - {cur_pos}

                if next_step in graph:
                    if next_step in edges:
                        edges[next_step] = max(num_steps, edges[next_step])
                    else:
                        edges[next_step] = num_steps

        return graph

    @functools.lru_cache(maxsize=None)
    def longest_path(self, start: Point, end: Point, remaining: Iterable[Point]) -> int:
        if start == end:
            return 0
        remaining = self.reachable(start, remaining)
        if end not in remaining:
            return -1

        longest: int = -1
        for next_node, distance in self.weighted_edges[start].items():
            if next_node in remaining:
                branch_length: int = self.longest_path(next_node, end, tuple(remaining))
                if branch_length != -1:
                    longest = max(longest, distance + branch_length)

        return longest

    def reachable(self, start: Point, nodes: Iterable[Point]) -> set[Point]:
        visited: set[Point] = set()
        to_visit: set[Point] = {start}
        while to_visit:
            cur_node: Point = to_visit.pop()
            visited.add(cur_node)
            to_visit |= (self.weighted_edges[cur_node].keys() & nodes) - visited

        visited.remove(start)
        return visited


def parse(puzzle_input):
    """Parse input"""
    return TrailMap(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    sorted_paths: list[Point] = sorted(data.paths.keys(), key=lambda pt: pt.y)
    return data.longest_path(sorted_paths[0], sorted_paths[-1], tuple(data.weighted_edges.keys()))


def part2(data):
    """Solve part 2"""
    data.melt_ice()
    return part1(data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 94
    PART2_TEST_ANSWER = 154

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
