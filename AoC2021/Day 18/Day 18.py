import pathlib
import sys
import os
from typing import Optional


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def snailfish_halves(sf: str) -> tuple[str, str]:
    sf = sf[1:-1]
    brackets: int = 0
    for i, ch in enumerate(sf):
        if ch == '[':
            brackets += 1
        elif ch == ']':
            brackets -= 1
        elif ch == ',' and brackets == 0:
            return sf[:i], sf[i + 1:]


class SnailfishNum:
    def __init__(self, num_str: str, parent: Optional['SnailfishNum'] = None) -> None:
        self.value: str = num_str
        self.left: Optional[SnailfishNum] = None
        self.right: Optional[SnailfishNum] = None
        self.parent: Optional[SnailfishNum] = parent
        if not num_str.isdigit():
            left, right = snailfish_halves(num_str)
            self.left = SnailfishNum(left, self)
            self.right = SnailfishNum(right, self)
            self.value = ','

    def __str__(self) -> str:
        if self.value.isdigit():
            return self.value
        return f'[{str(self.left)},{str(self.right)}]'

    def depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.depth() + 1

    def reduce(self) -> None:
        explode_target: Optional[SnailfishNum] = self.next_explode()
        split_target: Optional[SnailfishNum] = None
        if explode_target is None:
            split_target = self.next_split()

        while explode_target is not None or split_target is not None:
            if explode_target is not None:
                explode_target.explode()
            else:
                split_target.split()

            explode_target = self.next_explode()
            if explode_target is None:
                split_target = self.next_split()

    def next_explode(self) -> Optional['SnailfishNum']:
        if self.left:
            target: Optional[SnailfishNum] = self.left.next_explode()
            if target is not None:
                return target
        if self.value == ',' and self.depth() >= 4:
            return self
        if self.right:
            target = self.right.next_explode()
            if target is not None:
                return target

    def add_to_predecessor(self, n: int) -> None:
        cur_node: SnailfishNum = self
        while cur_node.parent:
            if cur_node.parent.right == cur_node:
                cur_node = cur_node.parent.left
                while cur_node.right:
                    cur_node = cur_node.right
                cur_node.value = str(int(cur_node.value) + n)
                return

            cur_node = cur_node.parent

    def add_to_successor(self, n: int) -> None:
        cur_node: SnailfishNum = self
        while cur_node.parent:
            if cur_node.parent.left == cur_node:
                cur_node = cur_node.parent.right
                while cur_node.left:
                    cur_node = cur_node.left
                cur_node.value = str(int(cur_node.value) + n)
                return

            cur_node = cur_node.parent

    def explode(self) -> None:
        self.add_to_predecessor(int(self.left.value))
        self.add_to_successor(int(self.right.value))
        self.left.parent = None
        self.right.parent = None
        self.left = None
        self.right = None
        self.value = '0'

    def next_split(self) -> Optional['SnailfishNum']:
        if self.left:
            target: Optional[SnailfishNum] = self.left.next_split()
            if target is not None:
                return target
        if self.value.isdigit() and int(self.value) >= 10:
            return self
        if self.right:
            target = self.right.next_split()
            if target is not None:
                return target

    def split(self) -> None:
        val: int = int(self.value)
        half: int = val // 2
        self.left = SnailfishNum(str(half), self)
        if val % 2 == 0:
            self.right = SnailfishNum(str(half), self)
        else:
            self.right = SnailfishNum(str(half + 1), self)
        self.value = ','

    def magnitude(self) -> int:
        if self.value.isdigit():
            return int(self.value)
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, other: 'SnailfishNum') -> 'SnailfishNum':
        sum_sfn: SnailfishNum = SnailfishNum(f'[{str(self)},{str(other)}]')
        sum_sfn.reduce()
        return sum_sfn

    def __iadd__(self, other: 'SnailfishNum') -> 'SnailfishNum':
        return self + other


def part1(data):
    """Solve part 1"""
    total: SnailfishNum = SnailfishNum(data[0])
    for line in data[1:]:
        total += SnailfishNum(line)
    return total.magnitude()


def part2(data):
    """Solve part 2"""
    max_mag: int = 0
    nums: list[SnailfishNum] = [SnailfishNum(line) for line in data]
    for i, sfn1 in enumerate(nums):
        for sfn2 in nums[i + 1:]:
            max_mag = max(max_mag, (sfn1 + sfn2).magnitude(), (sfn2 + sfn1).magnitude())
    return max_mag


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
