import pathlib
import sys
import os
from point import Point
from typing import Sequence, Iterable


class TrailMap:
    def __init__(self, trail_map: Sequence[str]) -> None:
        self.start: Point = Point(trail_map[0].index('.'), 0)
        self.end: Point = Point(trail_map[-1].index('.'), len(trail_map) - 1)
        self.paths: dict[Point, str] = {}
        self.neighbor_paths: dict[Point, set[Point]] = {}

        for y, line in enumerate(trail_map):
            for x, ch in enumerate(line):
                if ch != '#':
                    self.paths[Point(x, y)] = ch

        for path in self.paths:
            self.neighbor_paths[path] = path.neighbors() & self.paths.keys()

    def walkable(self, cur_pos: Point, target: Point) -> bool:
        if target == cur_pos.above():
            return self.paths[target] != 'v'
        if target == cur_pos.below():
            return self.paths[target] != '^'
        if target == cur_pos.left():
            return self.paths[target] != '>'
        if target == cur_pos.right():
            return self.paths[target] != '<'

    def longest_walk(self, cur_pos: Point, end: Point, prev_pos: Point = None, intersections: Iterable[Point] = None, dry: bool = False) -> int:
        if prev_pos is None:
            prev_pos = cur_pos.above()
        if intersections is None:
            intersections = set()
        else:
            intersections = set(intersections)

        num_steps: int = 0
        while cur_pos != end:
            num_steps += 1
            next_steps: set[Point] = self.neighbor_paths[cur_pos] - {prev_pos}

            if len(next_steps) > 1:
                intersections.add(cur_pos)
                if not dry:
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
                    return num_steps + max(self.longest_walk(step, end, cur_pos, intersections, dry) for step in next_steps)

        return num_steps


def parse(puzzle_input):
    """Parse input"""
    return TrailMap(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    return data.longest_walk(data.start, data.end)


def part2(data):
    """Solve part 2"""
    return data.longest_walk(data.start, data.end, dry=True)


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
