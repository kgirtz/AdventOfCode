import pathlib
import sys
import os
from collections.abc import Iterable, Collection

from xypair import XYpair


def parse(puzzle_input: str):
    """Parse input"""
    return [XYpair(*(int(n) for n in line.split(', '))) for line in puzzle_input.split('\n')]


def is_closest_coordinate(pt: XYpair, target: XYpair, coordinates: Iterable[XYpair]) -> bool:
    target_distance: int = pt.manhattan_distance(target)
    for coordinate in coordinates:
        if coordinate != target and pt.manhattan_distance(coordinate) <= target_distance:
            return False
    return True


def finite_area_size(pole: XYpair, coordinates: Iterable[XYpair]) -> int:
    min_x: int = min(pt.x for pt in coordinates)
    max_x: int = max(pt.x for pt in coordinates)
    min_y: int = min(pt.y for pt in coordinates)
    max_y: int = max(pt.y for pt in coordinates)

    area: set[XYpair] = set()
    to_check: set[XYpair] = {pole}
    while to_check:
        cur_pt: XYpair = to_check.pop()
        if not (min_x < cur_pt.x < max_x and min_y < cur_pt.y < max_y):
            return -1
        area.add(cur_pt)

        new_neighbors: set[XYpair] = cur_pt.neighbors().difference(coordinates) - area - to_check
        to_check.update(n for n in new_neighbors if is_closest_coordinate(n, pole, coordinates))

    return len(area)


def closest_to_all_coordinates(coordinates: Collection[XYpair], distance_sum: int) -> int:
    mass_center_x: int = sum(pt.x for pt in coordinates) // len(coordinates)
    mass_center_y: int = sum(pt.y for pt in coordinates) // len(coordinates)

    region: set[XYpair] = set()
    to_check: set[XYpair] = {XYpair(mass_center_x, mass_center_y)}
    while to_check:
        cur_pt: XYpair = to_check.pop()
        region.add(cur_pt)

        new_neighbors: set[XYpair] = cur_pt.neighbors() - region - to_check
        to_check.update(n for n in new_neighbors if sum(n.manhattan_distance(pt) for pt in coordinates) < distance_sum)

    return len(region)


def part1(data):
    """Solve part 1"""
    return max(finite_area_size(pole, data) for pole in data)


def part2(data):
    """Solve part 2"""
    return closest_to_all_coordinates(data, distance_sum=10000)  # test = 32, input = 10000


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 17
    PART2_TEST_ANSWER = None  # test = 16

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
