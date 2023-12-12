import pathlib
import sys
import os
from point import Point
from typing import Iterable, Sequence


def expand_galaxies(galaxies: Iterable[Point], expansion_rate: int) -> list[Point]:
    galaxy_rows: set[int] = {galaxy.y for galaxy in galaxies}
    galaxy_columns: set[int] = {galaxy.x for galaxy in galaxies}
    expansion_rows: set[int] = {r for r in range(max(galaxy_rows)) if r not in galaxy_rows}
    expansion_columns: set[int] = {c for c in range(max(galaxy_columns)) if c not in galaxy_columns}

    expanded: list[Point] = []
    for galaxy in galaxies:
        x: int = galaxy.x + (expansion_rate - 1) * len([c for c in expansion_columns if c < galaxy.x])
        y: int = galaxy.y + (expansion_rate - 1) * len([r for r in expansion_rows if r < galaxy.y])
        expanded.append(Point(x, y))
    return expanded


def sum_of_shortest_paths(galaxies: Sequence[Point]) -> int:
    path_sum: int = 0
    for i, source in enumerate(galaxies[:-1]):
        for j, destination in enumerate(galaxies[i + 1:]):
            path_sum += source.manhattan_distance(destination)
    return path_sum


def parse(puzzle_input):
    """Parse input"""
    galaxies: list[Point] = []
    for y, line in enumerate(puzzle_input.split('\n')):
        for x, pixel in enumerate(line):
            if pixel == '#':
                galaxies.append(Point(x, y))
    return galaxies


def part1(data):
    """Solve part 1"""
    return sum_of_shortest_paths(expand_galaxies(data, expansion_rate=2))


def part2(data):
    """Solve part 2"""
    return sum_of_shortest_paths(expand_galaxies(data, expansion_rate=1000000))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 374
    PART2_TEST_ANSWER = None

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
