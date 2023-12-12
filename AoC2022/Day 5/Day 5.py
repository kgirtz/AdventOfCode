import pathlib
import sys
import os
from collections import deque


def parse(puzzle_input):
    """Parse input"""
    stacks_str, steps_str = puzzle_input.split('\n\n')

    stack_lines: list[str] = stacks_str.split('\n')
    stacks: list[deque[str]] = [deque() for _ in stack_lines[-1].split()]
    for row in stack_lines[-2::-1]:
        for stack, crate in enumerate(row[1::4]):
            if crate != ' ':
                stacks[stack].append(crate)

    steps: list[tuple[int, int, int]] = []
    for step in steps_str.split('\n'):
        count, src, dst = (int(token) for token in step.split()[1::2])
        steps.append((count, src - 1, dst - 1))

    return stacks, steps


def part1(data):
    """Solve part 1"""
    stacks, steps = data

    for count, src, dst in steps:
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())

    return ''.join(d.pop() for d in stacks)


def part2(data):
    """Solve part 2"""
    stacks, steps = data

    temp_stack: deque[str] = deque()
    for count, src, dst in steps:
        temp_stack.clear()
        for _ in range(count):
            temp_stack.append(stacks[src].pop())
        for _ in range(count):
            stacks[dst].append(temp_stack.pop())

    return ''.join(d.pop() for d in stacks)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
