import pathlib
import sys
import os
import math


def parse(puzzle_input):
    """Parse input"""
    time_str, distance_str = puzzle_input.split('\n')
    times: list[int] = [int(t) for t in time_str.split()[1:]]
    distances: list[int] = [int(d) for d in distance_str.split()[1:]]
    big_time: int = int(''.join(time_str.split()[1:]))
    big_distance: int = int(''.join(distance_str.split()[1:]))
    return zip(times, distances), (big_time, big_distance)


def calculate_button_time(race_time: int, distance: int) -> tuple[float, float]:
    linear: float = race_time / 2
    root: float = math.sqrt(race_time * race_time - 4 * distance) / 2
    return round(linear - root, 5), round(linear + root, 5)


def count_ways_to_win(race_time: int, record: int) -> int:
    lo, hi = calculate_button_time(race_time, record)
    lo = math.ceil(lo) if math.ceil(lo) != lo else lo + 1
    hi = math.floor(hi) if math.floor(hi) != hi else hi - 1
    return int(hi - lo + 1)


def part1(data):
    """Solve part 1"""
    records, _ = data
    product: int = 1
    for t, d in records:
        product *= count_ways_to_win(t, d)
    return product


def part2(data):
    """Solve part 2"""
    _, (t, d) = data
    return count_ways_to_win(t, d)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 288
    PART2_TEST_ANSWER = 71503

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
