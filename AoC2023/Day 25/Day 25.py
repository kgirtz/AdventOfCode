import pathlib
import sys
import os
import random
from typing import Iterable
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    nodes: dict[str, set[str]] = defaultdict(set)
    edges: set[tuple[str, str]] = set()
    for line in puzzle_input.split('\n'):
        left, right_list = line.split(': ')
        for right in right_list.split():
            nodes[left].add(right)
            nodes[right].add(left)
            if not {(left, right), (right, left)} & edges:
                edges.add((left, right))
    return nodes, edges


def set_connections(left: set[str], right: set[str], edges: set[tuple[str, str]]) -> int:
    connections: int = 0
    for a, b in edges:
        if (a in left and b in right) or (b in left and a in right):
            connections += 1
    print(connections)
    return connections


def part1(data):
    """Solve part 1"""
    nodes, edges = data

    node_list: list[str] = list(nodes)
    num_nodes: int = len(node_list)

    left_nodes: set[str] = set()
    right_nodes: set[str] = set()

    while not left_nodes or not right_nodes:
        random.shuffle(node_list)

        left_nodes = set(node_list[:num_nodes // 2])
        right_nodes = set(node_list[num_nodes // 2:])

        left_to_right: set[str] = {n for n in left_nodes if not (nodes[n] & left_nodes)}
        left_nodes -= left_to_right
        right_nodes.update(left_to_right)

        right_to_left: set[str] = {n for n in right_nodes if not (nodes[n] & right_nodes)}
        right_nodes -= right_to_left
        left_nodes.update(right_to_left)

        while set_connections(left_nodes, right_nodes, edges) > 3:
            left_to_right = {n for n in left_nodes if nodes[n] & right_nodes}
            # left_to_right = {n for n in left_nodes if len(nodes[n] & right_nodes) > len(nodes[n] & left_nodes)}
            left_nodes -= left_to_right
            right_nodes.update(left_to_right)

            right_to_left = {n for n in right_nodes if nodes[n] & left_nodes}
            # right_to_left = {n for n in right_nodes if len(nodes[n] & left_nodes) > len(nodes[n] & right_nodes)}
            right_nodes -= right_to_left
            left_nodes.update(right_to_left)

            if not left_to_right and not right_to_left:
                left_to_right = {n for n in left_nodes if len(nodes[n] & right_nodes) == len(nodes[n] & left_nodes)}
                right_to_left = {n for n in right_nodes if len(nodes[n] & right_nodes) == len(nodes[n] & left_nodes)}
                if len(left_to_right) > len(right_to_left):
                    picked: str = left_to_right.pop()
                    left_nodes.remove(picked)
                    right_nodes.add(picked)
                elif right_to_left:
                    picked: str = right_to_left.pop()
                    right_nodes.remove(picked)
                    left_nodes.add(picked)

    return len(left_nodes) * len(right_nodes)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # 54

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
