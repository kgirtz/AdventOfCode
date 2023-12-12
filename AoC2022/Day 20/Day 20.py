import pathlib
import sys
import os
from typing import Optional


def parse(puzzle_input):
    """Parse input"""
    return [int(n) for n in puzzle_input.split()]


class Node:
    def __init__(self, n: int):
        self.val: int = n
        self.next: Node = self
        self.prev: Node = self

    def extract(self) -> None:
        self.next.prev = self.prev
        self.prev.next = self.next

    def insert_after(self, successor: 'Node') -> None:
        successor.next = self.next
        successor.prev = self
        self.next.prev = successor
        self.next = successor

    def shift(self, n: int, length: int) -> None:
        self.extract()
        target: Node = self.prev
        for _ in range(n % (length - 1)):
            target = target.next
        target.insert_after(self)

    def find(self, value: int) -> Optional['Node']:
        if self.val == value:
            return self

        cur_node: Node = self.next
        while cur_node is not self:
            if cur_node.val == value:
                return cur_node
            cur_node = cur_node.next

        return None

    def get_value_at(self, i: int) -> int:
        cur_node: Node = self
        for _ in range(i):
            cur_node = cur_node.next
        return cur_node.val


def mix(nodes: list[Node], count: int) -> None:
    num_nodes: int = len(nodes)
    for _ in range(count):
        for node in nodes:
            node.shift(node.val, num_nodes)


def decrypt(nodes: list[Node]) -> int:
    num_nodes: int = len(nodes)
    znode: Node = nodes[0].find(0)
    return sum(znode.get_value_at(d % num_nodes) for d in (1000, 2000, 3000))


def part1(data):
    """Solve part 1"""
    nodes: list[Node] = [Node(n) for n in data]
    for i, node in enumerate(nodes[:-1]):
        node.insert_after(nodes[i + 1])

    mix(nodes, 1)

    return decrypt(nodes)


def part2(data):
    """Solve part 2"""
    nodes: list[Node] = [Node(n * 811589153) for n in data]
    for i, node in enumerate(nodes[:-1]):
        node.insert_after(nodes[i + 1])

    mix(nodes, 10)

    return decrypt(nodes)


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
