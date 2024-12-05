import pathlib
import sys
import os
from typing import Sequence, Iterable, NamedTuple


class Rule(NamedTuple):
    first: int
    second: int

    def satisfied(self, s: Sequence[int]) -> bool:
        try:
            return s.index(self.first) < s.index(self.second)
        except ValueError:
            return True


def parse(puzzle_input: str):
    """Parse input"""
    rule_str, update_str = puzzle_input.split('\n\n')
    rules: list[tuple[int, ...]] = [Rule(*(int(u) for u in r.split('|'))) for r in rule_str.split('\n')]
    updates: list[list[int]] = [[int(n) for n in update.split(',')] for update in update_str.split('\n')]
    return rules, updates


def middle(s: Sequence[int]) -> int:
    return s[len(s) // 2]


def in_correct_order(update: Sequence[int], rules: Iterable[Rule]) -> bool:
    return all(rule.satisfied(update) for rule in rules)


def fix(update: Sequence[int], rules: Iterable[Rule]) -> list[int]:
    update = list(update)
    while not in_correct_order(update, rules):
        for rule in rules:
            if not rule.satisfied(update):
                i: int = update.index(rule.first)
                j: int = update.index(rule.second)
                update[i], update[j] = update[j], update[i]
    return update


def part1(data):
    """Solve part 1"""
    rules, updates = data
    return sum(middle(update) for update in updates if in_correct_order(update, rules))


def part2(data):
    """Solve part 2"""
    rules, updates = data
    return sum(middle(fix(update, rules)) for update in updates if not in_correct_order(update, rules))


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 143
    PART2_TEST_ANSWER = 123

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
