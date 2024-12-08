import itertools
import pathlib
import sys
import os
from collections import defaultdict

from numpy.random.mtrand import Sequence

from point import Point
from space import Space


turn_right: dict[str, str] = {'^': '>',
                              '>': 'v',
                              'v': '<',
                              '<': '^'}


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.split('\n')


def get_next(pos: Point, direction: str) -> Point:
    match direction:
        case '^':
            return pos.above()
        case '>':
            return pos.right()
        case 'v':
            return pos.below()
        case '<':
            return pos.left()
        case _:
            raise ValueError('invalid direction')


def next_stop(pos: Point, direction: str, s: Space) -> (Point, str):
    match direction:
        case '^':
            objects: list[int] = sorted((pt.y + 1 for pt in s.items['#'] if pt.x == pos.x and pt.y < pos.y))
            stop: Point = Point(pos.x, objects[-1] if objects else 0)
            return stop, '>'
        case '>':
            objects: list[int] = sorted((pt.x - 1 for pt in s.items['#'] if pt.x > pos.x and pt.y == pos.y))
            stop: Point = Point(objects[0] if objects else s.width - 1, pos.y)
            return stop, 'v'
        case 'v':
            objects: list[int] = sorted((pt.y - 1 for pt in s.items['#'] if pt.x == pos.x and pt.y > pos.y))
            stop: Point = Point(pos.x, objects[0] if objects else s.height - 1)
            return stop, '<'
        case '<':
            objects: list[int] = sorted((pt.x + 1 for pt in s.items['#'] if pt.x < pos.x and pt.y == pos.y))
            stop: Point = Point(objects[-1] if objects else 0, pos.y)
            return stop, '^'


def path(s: Space) -> set[Point]:
    visited: set[Point] = set()
    cur_dir: str = '^'
    cur_pos: Point = s.initial_position(cur_dir)
    while s.valid_point(cur_pos):
        visited.add(cur_pos)
        next_pos: Point = get_next(cur_pos, cur_dir)
        while next_pos in s.items['#']:
            cur_dir = turn_right[cur_dir]
            next_pos = get_next(cur_pos, cur_dir)
        cur_pos = next_pos
    return visited


def path_turns(s: Space) -> list[Point]:
    cur_dir: str = '^'
    cur_pos: Point = s.initial_position(cur_dir)
    turns: list[Point] = [cur_pos]
    while True:
        cur_pos, cur_dir = next_stop(cur_pos, cur_dir, s)
        turns.append(cur_pos)
        if s.on_edge(cur_pos):
            return turns


def path_length(turns: Sequence[Point]) -> int:
    return sum(start.manhattan_distance(end) - 1 for start, end in itertools.pairwise(turns)) + 1


def loops(s: Space) -> bool:
    visited: dict[Point, set[str]] = defaultdict(set)
    cur_dir: str = '^'
    cur_pos: Point = s.initial_position(cur_dir)
    while s.valid_point(cur_pos):
        visited[cur_pos].add(cur_dir)
        next_pos: Point = get_next(cur_pos, cur_dir)
        while next_pos in s.items['#']:
            cur_dir = turn_right[cur_dir]
            next_pos = get_next(cur_pos, cur_dir)
        cur_pos = next_pos

        if cur_dir in visited[cur_pos]:
            return True

    return False


def part1(data):
    """Solve part 1"""
    s: Space = Space(data)

    return len(path(s))


def part2(data):
    """Solve part 2"""  # 1920 is too high
    s: Space = Space(data)

    num_loops: int = 0
    possible: set[Point] = path(s) - {s.initial_position('^')}
    for pt in possible:
        s.items['#'].add(pt)
        if loops(s):
            num_loops += 1
        s.items['#'].remove(pt)
    return num_loops


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 41
    PART2_TEST_ANSWER = 6

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
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

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
