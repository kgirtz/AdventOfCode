import pathlib
import sys
import os
import re
from typing import Sequence

Part = dict[str, int]


class Workflow:
    def __init__(self, rules: Sequence[str]) -> None:
        self.rules: list[str] = list(rules)

    def process(self, part: Part) -> str:
        for rule in self.rules:
            if ':' not in rule:
                return rule

            condition, destination = rule.split(':')
            if self.evaluate(condition, part):
                return destination

    @staticmethod
    def evaluate(condition: str, part: Part) -> bool:
        if '<' in condition:
            category, value = condition.split('<')
            return part[category] < int(value)
        elif '>' in condition:
            category, value = condition.split('>')
            return part[category] > int(value)


def parse(puzzle_input):
    """Parse input"""
    workflow_str, rating_str = puzzle_input.split('\n\n')

    workflows: dict[str, Workflow] = {}
    for line in workflow_str.split('\n'):
        name, rules = re.match(r'(.+)\{(.+)\}', line).groups()
        workflows[name] = Workflow(rules.split(','))

    ratings: list[Part] = []
    for line in rating_str.split('\n'):
        part: Part = {}
        for rating in line.strip('{}').split(','):
            category, value = rating.split('=')
            part[category] = int(value)
        ratings.append(part)

    return workflows, ratings


def accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    next_workflow: str = 'in'
    while next_workflow not in ('A', 'R'):
        next_workflow = workflows[next_workflow].process(part)
    return next_workflow == 'A'


def number_accepted(bottom: Part, top: Part, workflows: dict[str, Workflow], cur_flow: str = 'in') -> int:
    if cur_flow == 'R' or any(top[c] < bottom[c] for c in top):
        return 0
    if cur_flow == 'A':
        combos: int = 1
        for category in bottom:
            combos *= top[category] - bottom[category] + 1
        return combos

    total_combos: int = 0
    for rule in workflows[cur_flow].rules:
        if ':' not in rule:
            return total_combos + number_accepted(bottom.copy(), top.copy(), workflows, rule)

        condition, destination = rule.split(':')
        if '<' in condition:
            category, value = condition.split('<')
            new_top: Part = top.copy()
            new_top[category] = int(value) - 1
            total_combos += number_accepted(bottom.copy(), new_top, workflows, destination)
            bottom[category] = int(value)
        elif '>' in condition:
            category, value = condition.split('>')
            new_bottom: Part = bottom.copy()
            new_bottom[category] = int(value) + 1
            total_combos += number_accepted(new_bottom, top.copy(), workflows, destination)
            top[category] = int(value)


def part1(data):
    """Solve part 1"""
    workflows, parts = data
    accepted_parts: list[Part] = [p for p in parts if accepted(p, workflows)]
    return sum(sum(p.values()) for p in accepted_parts)


def part2(data):
    """Solve part 2"""
    workflows, _ = data
    return number_accepted({c: 1 for c in 'xmas'}, {c: 4000 for c in 'xmas'}, workflows)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 19114
    PART2_TEST_ANSWER = 167409079868000

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
