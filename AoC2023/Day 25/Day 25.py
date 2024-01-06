import pathlib
import sys
import os
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


def expand(to_expand: set[str], nodes: dict[str, set[str]], min_connections: int = 0) -> set[str]:
    expanded_nodes: set[str] = to_expand.copy()
    while to_expand:
        cur_node: str = to_expand.pop()
        expanded_nodes.add(cur_node)
        for neighbor in nodes[cur_node] - expanded_nodes:
            if len(nodes[neighbor] & expanded_nodes) >= min_connections:
                to_expand.add(neighbor)
    return expanded_nodes


def connected_components(nodes: dict[str, set[str]]) -> list[set[str]]:
    components: list[set[str]] = []
    
    remaining_nodes: set[str] = set(nodes.keys())
    while remaining_nodes:
        cur_component: set[str] = expand({remaining_nodes.pop()}, nodes)
        components.append(cur_component)
        remaining_nodes -= cur_component
        
    return components


def independent_groups(nodes: dict[str, set[str]]) -> (set[str], set[str]):
    node_list: list[str] = list(nodes)
    num_nodes: int = len(node_list)
    
    if num_nodes == 1:
        return {node_list[0]}, set()
    
    components: list[set[str]] = connected_components(nodes)
    if len(components) >= 2:
        components.sort(key=lambda s: len(s), reverse=True)
        return tuple(components[:2])
    
    half_nodes: set[str] = set(node_list[:num_nodes // 2])
    return independent_groups({n: nodes[n] & half_nodes for n in half_nodes})


def part1(data):
    """Solve part 1"""
    nodes, edges = data
    
    left, right = independent_groups(nodes)
    left = expand(left, nodes, 2)
    right = expand(right, nodes, 2)
    
    # Purge uncuttable edges
    edges_to_try: list[tuple[str, str]] = [e for e in edges if not set(e).issubset(left) and not set(e).issubset(right)]
    
    # Brute force remaining potential edges
    for i, (c1a, c1b) in enumerate(edges_to_try[:-2]):
        nodes[c1a].remove(c1b)
        nodes[c1b].remove(c1a)
        for j, (c2a, c2b) in enumerate(edges_to_try[i + 1:-1], i + 1):
            nodes[c2a].remove(c2b)
            nodes[c2b].remove(c2a)
            for (c3a, c3b) in edges_to_try[j + 1:]:
                nodes[c3a].remove(c3b)
                nodes[c3b].remove(c3a)
                
                if c3a not in expand({c3b}, nodes):
                    left, right = connected_components(nodes)
                    return len(left) * len(right)
                    
                nodes[c3a].add(c3b)
                nodes[c3b].add(c3a)
            nodes[c2a].add(c2b)
            nodes[c2b].add(c2a)
        nodes[c1a].add(c1b)
        nodes[c1b].add(c1a)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 54

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
