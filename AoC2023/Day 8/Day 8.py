import pathlib
import sys
import os
import re
import dataclasses
import math


def parse(puzzle_input):
    """Parse input"""
    instructions, node_str = puzzle_input.split('\n\n')
    nodes: dict[str, dict[str, str]] = {}
    for line in node_str.split('\n'):
        m: re.Match = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)
        nodes[m.group(1)] = {'L': m.group(2), 'R': m.group(3)}
    return instructions, Network(nodes)


@dataclasses.dataclass
class Network:
    nodes: dict[str, dict[str, str]]

    def hop(self, origin: str, instruction: str) -> str:
        return self.nodes[origin][instruction]

    def traverse(self, origin: str, destination: str, instructions: str) -> int:
        current: str = origin
        num_steps: int = 0
        while current != destination:
            current = self.hop(current, instructions[num_steps % len(instructions)])
            num_steps += 1
        return num_steps

    def ghost_traverse(self, origin: str, instructions: str) -> int:
        current: str = origin
        num_steps: int = 0
        while not current.endswith('Z'):
            current = self.hop(current, instructions[num_steps % len(instructions)])
            num_steps += 1
        return num_steps


def part1(data):
    """Solve part 1"""
    instructions, network = data
    return network.traverse('AAA', 'ZZZ', instructions)


def part2(data):
    """Solve part 2"""
    instructions, network = data
    starting_nodes: list[str] = list({node for node in network.nodes if node.endswith('A')})
    hop_counts: list[int] = [network.ghost_traverse(node, instructions) for node in starting_nodes]
    return math.lcm(*hop_counts)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 6
    PART2_TEST_ANSWER = 6

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
