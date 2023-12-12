import pathlib
import sys
import os
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    return [tuple(line.split('-')) for line in puzzle_input.split('\n')]


def graph(edges: list[tuple[str, str]]) -> dict[str, set[str]]:
    system: defaultdict[str, set[str]] = defaultdict(set)
    for v1, v2 in edges:
        system[v1].add(v2)
        system[v2].add(v1)
    return dict(system)


def paths(context: str, graph: dict[str, set[str]], use_lower_twice: bool = False) -> set[str]:
    possible_paths: set[str] = set()
    cur_v: str = context.split(',')[-1]

    if cur_v != 'end':
        for v in graph[cur_v]:
            if v == 'start':
                continue
            elif v == 'end':
                possible_paths.add(f'{context},end')
            elif v.islower() and v in context:
                if use_lower_twice:
                    possible_paths.update(paths(f'{context},{v}', graph, False))
            else:
                possible_paths.update(paths(f'{context},{v}', graph, use_lower_twice))

    return possible_paths


def part1(data):
    """Solve part 1"""
    caves: dict[str, set[str]] = graph(data)
    return len(paths('start', caves))


def part2(data):
    """Solve part 2"""
    caves: dict[str, set[str]] = graph(data)
    return len(paths('start', caves, True))


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
