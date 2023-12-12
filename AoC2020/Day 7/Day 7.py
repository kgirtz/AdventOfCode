import pathlib
import sys
import os
import parse as scanf


def parse(puzzle_input):
    """Parse input"""
    return parse_rules([line for line in puzzle_input.split('\n')])


def parse_rules(rules: list[str]) -> dict[str, dict[str, int]]:
    rule_dict: dict[str, dict[str, int]] = {}
    for rule in rules:
        color, contents = scanf.parse('{} bags contain {}.', rule)
        rule_dict[color] = {}
        if contents != 'no other bags':
            for inner_bag in contents.split(','):
                amount, inner_color = scanf.search('{:d} {} bag', inner_bag)
                rule_dict[color][inner_color] = amount
    return rule_dict


def can_hold_color(rules: dict[str, dict[str, int]], outer: str, color: str) -> bool:
    if color in rules[outer]:
        return True
    return any(can_hold_color(rules, inner, color) for inner in rules[outer])


def bags_inside(rules: dict[str, dict[str, int]], outer: str) -> int:
    total: int = 0
    for color, count in rules[outer].items():
        total += count * (bags_inside(rules, color) + 1)
    return total


def part1(data):
    """Solve part 1"""
    holds_shiny_gold: int = 0
    for color in data:
        if can_hold_color(data, color, 'shiny gold'):
            holds_shiny_gold += 1
    return holds_shiny_gold


def part2(data):
    """Solve part 2"""
    return bags_inside(data, 'shiny gold')


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
