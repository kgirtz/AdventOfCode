import pathlib
import sys
import os
import collections
from typing import Iterable


def parse(puzzle_input: str):
    """Parse input"""
    return [line.split('-') for line in puzzle_input.split('\n')]


def network_graph(connections: Iterable[Iterable[str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = collections.defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)
    return graph


def interconnected_trios(graph: dict[str, set[str]]) -> set[tuple[str, str, str]]:
    trios: set[tuple[str, str, str]] = set()
    for node, connections in graph.items():
        connections = list(connections)
        for i, first in enumerate(connections[:-1]):
            for second in connections[i + 1:]:
                if second in graph[first]:
                    trios.add(tuple(sorted((node, first, second))))  # noqa
    return trios


def part1(data):
    """Solve part 1"""
    total: int = 0
    for trio in interconnected_trios(network_graph(data)):
        if any(name.startswith('t') for name in trio):
            total += 1
    return total


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 7
    PART2_TEST_ANSWER = 'co,de,ka,ta'

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
