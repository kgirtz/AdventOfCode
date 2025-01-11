import pathlib
import sys
import os
import collections
import heapq
from collections.abc import Iterable, Mapping


def parse(puzzle_input: str):
    """Parse input"""
    return [(line.split()[1], line.split()[7]) for line in puzzle_input.split('\n')]


def prereq_dictionary(rules: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    steps: dict[str, set[str]] = collections.defaultdict(set)
    for first, second in rules:
        steps[second].add(first)
        if first not in steps:
            steps[first] = set()
    return steps


def nonparallel_order(steps: Mapping[str, set[str]]) -> str:
    steps = dict(steps)
    order: str = ''
    while steps:
        ready: set[str] = {s for s, prereqs in steps.items() if not prereqs.difference(order)}
        next_step: str = min(ready)
        order += next_step
        steps.pop(next_step)
    return order


def duration(step: str) -> int:
    # return ord(step) - 64  # test = ord(step) - ord('A') + 1
    return ord(step) - 4  # input = 60 + ord(step) - ord('A') + 1


def parallel_time(steps: Mapping[str, set[str]], num_workers: int) -> int:
    steps = dict(steps)

    workers: list[tuple[int, str]] = [(0, '_') for _ in range(num_workers)]

    completed: set[str] = set()
    while steps:
        start_time, step_completed = heapq.heappop(workers)
        if step_completed != '_':
            completed.add(step_completed)

        ready: set[str] = {s for s, prereqs in steps.items() if not prereqs.difference(completed)}
        if not ready:
            next_completed: int = min(done_time for done_time, task in workers if task != '_')
            heapq.heappush(workers, (next_completed, '_'))
            continue

        next_step: str = min(ready)
        steps.pop(next_step)
        heapq.heappush(workers, (start_time + duration(next_step), next_step))

    return max(workers)[0]


def part1(data):
    """Solve part 1"""
    steps: Mapping[str, set[str]] = prereq_dictionary(data)
    return nonparallel_order(steps)


def part2(data):
    """Solve part 2"""
    steps: Mapping[str, set[str]] = prereq_dictionary(data)
    return parallel_time(steps, 5)  # test = 2, input = 5


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 'CABDFE'
    PART2_TEST_ANSWER = None  # test = 15

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
