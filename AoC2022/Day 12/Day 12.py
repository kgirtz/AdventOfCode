import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def convert_heights_to_int(hmap: list[str]) -> tuple[Point, Point, list[list[int]]]:
    def char_to_height(ch: str) -> int:
        return ord(ch) - ord('a')

    h: int = len(hmap)
    w: int = len(hmap[0])

    start: Point = Point(0, 0)
    end: Point = Point(0, 0)
    num_hmap: list[list[int]] = [[0 for _ in range(w)] for _ in range(h)]

    for y, row in enumerate(hmap):
        for x, sym in enumerate(row):
            match sym:
                case 'S':
                    start = Point(x, y)
                    num_hmap[y][x] = char_to_height('a')
                case 'E':
                    end = Point(x, y)
                    num_hmap[y][x] = char_to_height('z')
                case _:
                    num_hmap[y][x] = char_to_height(sym)

    return start, end, num_hmap


def valid_moves(pt: Point, hmap: list[list[int]]) -> set[Point]:
    x_max: int = len(hmap[0]) - 1
    y_max: int = len(hmap) - 1
    h: int = hmap[pt.y][pt.x]

    neighbors: set[Point] = set()

    # Left
    if pt.x > 0 and hmap[pt.y][pt.x - 1] <= h + 1:
        neighbors.add(Point(pt.x - 1, pt.y))

    # Right
    if pt.x < x_max and hmap[pt.y][pt.x + 1] <= h + 1:
        neighbors.add(Point(pt.x + 1, pt.y))

    # Up
    if pt.y > 0 and hmap[pt.y - 1][pt.x] <= h + 1:
        neighbors.add(Point(pt.x, pt.y - 1))

    # Down
    if pt.y < y_max and hmap[pt.y + 1][pt.x] <= h + 1:
        neighbors.add(Point(pt.x, pt.y + 1))

    return neighbors


def fewest_steps(start: Point, end: Point, hmap: list[list[int]]) -> int:
    iteration: int = 0
    finished: dict[Point, int] = {}
    checking: set[Point] = {start}

    while end not in finished and checking:
        check_next: set[Point] = set()
        while checking:
            cur_point: Point = checking.pop()

            check_next |= valid_moves(cur_point, hmap)
            finished[cur_point] = iteration

        checking = check_next - finished.keys()
        iteration += 1

    if end in finished:
        return finished[end]
    else:
        return -1


def part1(data):
    """Solve part 1"""
    start, end, hmap = convert_heights_to_int(data)

    return fewest_steps(start, end, hmap)


def part2(data):
    """Solve part 2"""
    _, end, hmap = convert_heights_to_int(data)

    width: int = len(hmap[0])
    length: int = len(hmap)

    starting_points: set[Point] = {Point(x, y) for x in range(width) for y in range(length) if hmap[y][x] == 0}

    best_start: int = width * length
    for s in starting_points:
        steps: int = fewest_steps(s, end, hmap)
        if steps >= 0:
            best_start = min(best_start, steps)

    return best_start


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
