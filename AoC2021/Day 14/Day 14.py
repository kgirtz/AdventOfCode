import pathlib
import sys
import os
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    template, rules = puzzle_input.split('\n\n')

    rule_dict: dict[str, str] = {}
    for rule in rules.split('\n'):
        pair, insert = rule.split(' -> ')
        rule_dict[pair] = insert

    return template, rule_dict


def polymer_to_dict(polymer: str) -> dict[str, int]:
    p_dict: defaultdict[str, int] = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair: str = polymer[i:i + 2]
        p_dict[pair] += 1
    return dict(p_dict)


def pair_insertion(polymer: dict[str, int], rules: dict[str, str]) -> dict[str, int]:
    new_polymer: defaultdict[str, int] = defaultdict(int)
    for pair in polymer:
        insertion_element: str = rules[pair]
        pair1: str = f'{pair[0]}{insertion_element}'
        pair2: str = f'{insertion_element}{pair[1]}'
        new_polymer[pair1] += polymer[pair]
        new_polymer[pair2] += polymer[pair]
    return dict(new_polymer)


def count_elements(polymer: dict[str, int], last_ch: str) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for pair in polymer:
        element: str = pair[0]
        counts[element] += polymer[pair]
    counts[last_ch] += 1
    return dict(counts)


def part1(data):
    """Solve part 1"""
    polymer_template, insertion_rules = data
    polymer_dict: dict[str, int] = polymer_to_dict(polymer_template)
    for _ in range(10):
        polymer_dict = pair_insertion(polymer_dict, insertion_rules)
    element_counts: dict[str, int] = count_elements(polymer_dict, polymer_template[-1])
    return max(element_counts.values()) - min(element_counts.values())


def part2(data):
    """Solve part 2"""
    polymer_template, insertion_rules = data
    polymer_dict: dict[str, int] = polymer_to_dict(polymer_template)
    for _ in range(40):
        polymer_dict = pair_insertion(polymer_dict, insertion_rules)
    element_counts: dict[str, int] = count_elements(polymer_dict, polymer_template[-1])
    return max(element_counts.values()) - min(element_counts.values())


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
