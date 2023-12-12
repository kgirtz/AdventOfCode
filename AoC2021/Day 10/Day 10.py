import pathlib
import sys
import os
from typing import Optional


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def corrupted(line: str) -> Optional[str]:
    opens: str = '([{<'
    closes: str = ')]}>'
    brackets: dict[str, str] = {c: o for o, c in zip(opens, closes)}

    stack: list[str] = []
    for b in line:
        if b in opens:
            stack.append(b)
        elif b in closes:
            if stack.pop() != brackets[b]:
                return b


def complete(line: str) -> str:
    opens: str = '([{<'
    closes: str = ')]}>'
    brackets: dict[str, str] = {o: c for o, c in zip(opens, closes)}

    stack: list[str] = []
    for b in line:
        if b in opens:
            stack.append(b)
        elif b in closes:
            stack.pop()

    return ''.join(brackets[o] for o in reversed(stack))


def corruption_score(ch: str) -> int:
    scores: dict[str, int] = {')': 3,
                              ']': 57,
                              '}': 1197,
                              '>': 25137}
    return scores.get(ch, 0)


def completion_score(end: str) -> int:
    scores: dict[str, int] = {')': 1,
                              ']': 2,
                              '}': 3,
                              '>': 4}
    score: int = 0
    for ch in end:
        score = 5 * score + scores[ch]
    return score


def part1(data):
    """Solve part 1"""
    total_score: int = 0
    for line in data:
        bad_ch: Optional[str] = corrupted(line)
        if bad_ch is not None:
            total_score += corruption_score(bad_ch)
    return total_score


def part2(data):
    """Solve part 2"""
    incomplete_lines: list[str] = [line for line in data if corrupted(line) is None]
    completions: list[str] = [complete(line) for line in incomplete_lines]
    scores: list[int] = sorted(completion_score(c) for c in completions)
    middle: int = len(scores) // 2
    return scores[middle]


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
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
