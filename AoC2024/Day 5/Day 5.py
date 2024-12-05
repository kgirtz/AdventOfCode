import pathlib
import sys
import os


def parse(puzzle_input: str):
    """Parse input"""
    rule_str, update_str = puzzle_input.split('\n\n')
    rules: list[tuple[int, ...]] = [tuple(int(u) for u in r.split('|')) for r in rule_str.split('\n')]
    updates: list[list[int]] = [[int(n) for n in update.split(',')] for update in update_str.split('\n')]
    return rules, updates


def satisfies_rule(update: list[int], rule: tuple[int, int]) -> bool:
    first, second = rule
    if first not in update or second not in update:
        return True
    return update.index(first) < update.index(second)


def in_correct_order(update: list[int], rules: list[tuple[int, int]]) -> bool:
    return all(satisfies_rule(update, rule) for rule in rules)


def fix(update, rules) -> list[int]:
    rules = [r for r in rules if len(set(r) & set(update)) == 2]
    while not in_correct_order(update, rules):
        for first, second in rules:
            i_first: int = update.index(first)
            i_second: int = update.index(second)
            if i_first > i_second:
                update[i_first] = second
                update[i_second] = first
    return update


def part1(data):
    """Solve part 1"""
    rules, updates = data

    total: int = 0
    for update in updates:
        if in_correct_order(update, rules):
            total += update[len(update) // 2]
    return total


def part2(data):
    """Solve part 2"""
    rules, updates = data

    total: int = 0
    for update in updates:
        if not in_correct_order(update, rules):
            correct_order: list[int] = fix(update, rules)
            total += correct_order[len(correct_order) // 2]
    return total


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
