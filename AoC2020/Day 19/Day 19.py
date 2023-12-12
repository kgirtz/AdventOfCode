import pathlib
import sys
import os
import parse as scanf


def parse(puzzle_input):
    """Parse input"""
    rules, messages = puzzle_input.split('\n\n')
    return rules.split('\n'), messages.split()


class MessageValidater:
    def __init__(self, rule_strs: list[str]) -> None:
        self.rules: dict[int, tuple] = {}
        self.cache: dict[tuple[int, str], bool] = {}
        for rule_str in rule_strs:
            rule_num, rule = scanf.parse('{:d}: {}', rule_str)
            if rule in ('"a"', '"b"'):
                self.rules[rule_num] = tuple(rule.strip('"'))
            else:
                self.rules[rule_num] = tuple(tuple(int(s) for s in sub.split()) for sub in rule.split('|'))

        self.min_length: dict[int, int] = {}
        for rule in self.rules:
            if rule not in self.min_length:
                self.min_length[rule] = self.determine_min_length(rule)

    def determine_min_length(self, rule_num: int) -> int:
        rule: tuple = self.rules[rule_num]
        if rule[0] == 'a' or rule[0] == 'b':
            return 1

        min_length: int = 1000
        for option in rule:
            min_option_length: int = 0
            for sub_rule in option:
                if sub_rule != rule_num:
                    min_option_length += self.determine_min_length(sub_rule)
            min_length = min(min_length, min_option_length)
        return min_length

    def matches_sub_rules(self, message: str, sub_rules: tuple):
        if len(sub_rules) == 1:
            return self.matches_rule(message, sub_rules[0])

        start: int = self.min_length[sub_rules[0]]
        end: int = len(message) - sum(self.min_length[sub] for sub in sub_rules[1:])
        for i in range(start, end + 1):
            if self.matches_rule(message[:i], sub_rules[0]) and self.matches_sub_rules(message[i:], sub_rules[1:]):
                return True
        return False

    def matches_rule(self, message: str, rule_num: int) -> bool:
        if (rule_num, message) in self.cache:
            return self.cache[(rule_num, message)]

        if len(message) < self.min_length[rule_num]:
            self.cache[(rule_num, message)] = False
            return False

        rule: tuple = self.rules[rule_num]
        if rule[0] == 'a' or rule[0] == 'b':
            result: bool = (message == rule[0])
            self.cache[(rule_num, message)] = result
            return result

        for sub_rule_list in rule:
            if self.matches_sub_rules(message, sub_rule_list):
                self.cache[(rule_num, message)] = True
                return True

        self.cache[(rule_num, message)] = False
        return False

    def valid(self, message: str) -> bool:
        return self.matches_rule(message, 0)


def part1(data):
    """Solve part 1"""
    rules, messages = data
    parser: MessageValidater = MessageValidater(rules)
    matches: int = 0
    for message in messages:
        if parser.valid(message):
            matches += 1
    return matches


def part2(data):
    """Solve part 2"""
    rules, messages = data

    idx: int = rules.index('8: 42')
    rules[idx] = '8: 42 | 42 8'
    idx = rules.index('11: 42 31')
    rules[idx] = '11: 42 31 | 42 11 31'

    parser: MessageValidater = MessageValidater(rules)
    matches: int = 0
    for message in messages:
        if parser.valid(message):
            matches += 1
    return matches


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
        puzzle_input = pathlib.Path('./' + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
