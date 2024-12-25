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


def fully_connected_trios(graph: dict[str, set[str]]) -> set[frozenset[str]]:
    trios: set[frozenset[str]] = set()
    for node, connections in graph.items():
        connections = tuple(connections)
        for i, first in enumerate(connections[:-1]):
            for second in connections[i + 1:]:
                if second in graph[first]:
                    trios.add(frozenset((node, first, second)))
    return trios


def largest_fully_connected_group(graph: dict[str, set[str]]) -> set[str]:
    groups: set[frozenset[str]] = fully_connected_trios(graph)
    largest_group: set[str] = set()
    for trio in groups:
        expanded: set[str] = fully_connected_group(trio, graph)
        if len(expanded) > len(largest_group):
            largest_group = expanded
    return largest_group


def fully_connected_group(group: Iterable[str], graph: dict[str, set[str]]) -> set[str]:
    node: str = tuple(group)[0]
    full_group: set[str] = set(group)
    possible_members: set[str] = graph[node].difference(group)
    while possible_members:
        member: str = possible_members.pop()
        if full_group.issubset(graph[member]):
            full_group.add(member)
    return full_group


def password(computers: Iterable[str]) -> str:
    return ','.join(sorted(computers))


def part1(data):
    """Solve part 1"""
    graph: dict[str, set[str]] = network_graph(data)
    return sum(any(name.startswith('t') for name in trio) for trio in fully_connected_trios(graph))


def part2(data):
    """Solve part 2"""
    graph: dict[str, set[str]] = network_graph(data)
    return password(largest_fully_connected_group(graph))


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
