import pathlib
import sys
import os
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
        if target == cur_pos.above():
            return self.paths[target] != 'v'
        if target == cur_pos.below():
            return self.paths[target] != '^'
        if target == cur_pos.left():
            return self.paths[target] != '>'
        if target == cur_pos.right():
            return self.paths[target] != '<'

    def make_graph(self) -> dict[Point, dict[Point, int]]:
        outgoing: dict[Point, set[Point]] = defaultdict(set)
        for path, path_type in self.paths:
            match path_type:
                case '^':
                    if self.paths.get(path.above(), '#') not in ('v', '#'):
                        outgoing[path].add(path.above())
                case 'v':
                    if self.paths.get(path.below(), '#') not in ('^', '#'):
                        outgoing[path].add(path.below())
                case '<':
                    if self.paths.get(path.left(), '#') not in ('>', '#'):
                        outgoing[path].add(path.left())
                case '>':
                    if self.paths.get(path.right(), '#') not in ('<', '#'):
                        outgoing[path].add(path.right())
                case _:
                    for n in path.neighbors():
                        if n in self.paths and self.walkable(path, n):
                            outgoing[path].add(n)

        sorted_paths: list[Point] = sorted(self.paths.keys(), key=lambda pt: pt.y)
        start: Point = sorted_paths[0]
        end: Point = sorted_paths[-1]

        graph: dict[Point, dict[Point, int]] = {p: {} for p in self.paths if len(outgoing[p]) > 1 or p in (start, end)}
        for node, edges in graph.items():
            cur_pos: Point = node
            for next_step in outgoing[node]:
                num_steps: int = 1
                next_steps: set[Point] = outgoing[next_step] - {cur_pos}
                while len(next_steps) == 1:
                    num_steps += 1
                    cur_pos = next_step
                    next_step = list(next_steps)[0]

                if len(outgoing[next_step]) > 0 or next_step in (start, end):
                    edges[next_step] = num_steps




        return graph

    def longest_walk(self, cur_pos: Point, end: Point, prev_pos: Point = None, intersections: Iterable[Point] = None) -> int:
        if prev_pos is None:
            prev_pos = cur_pos.above()
        if intersections is None:
            intersections = set()
        else:
            intersections = set(intersections)

        num_steps: int = 0
        while cur_pos != end:
            num_steps += 1
            next_steps: set[Point] = (cur_pos.neighbors() & self.paths.keys()) - {prev_pos}

            if len(next_steps) > 1:
                intersections.add(cur_pos)
                match self.paths[cur_pos]:
                    case '.':
                        next_steps = {step for step in next_steps if self.walkable(cur_pos, step)}
                    case '^':
                        next_steps = {cur_pos.above()}
                    case 'v':
                        next_steps = {cur_pos.below()}
                    case '<':
                        next_steps = {cur_pos.left()}
                    case '>':
                        next_steps = {cur_pos.right()}

            next_steps -= intersections

            match len(next_steps):
                case 0:
                    return 0
                case 1:
                    prev_pos, cur_pos = cur_pos, next_steps.pop()
                case _:
                    return num_steps + max(self.longest_walk(step, end, cur_pos, intersections) for step in next_steps)

        return num_steps


def parse(puzzle_input):
    """Parse input"""
    return TrailMap(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    sorted_paths: list[Point] = sorted(data.paths.keys(), key=lambda pt: pt.y)
    return data.longest_walk(sorted_paths[0], sorted_paths[-1])


def part2(data):
    """Solve part 2"""
    data.melt_ice()
    return part1(data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = None # part2(data)

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
