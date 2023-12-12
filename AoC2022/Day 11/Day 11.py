import pathlib
import sys
import os
from collections import defaultdict


class Monkey:
    def __init__(self, note: str):
        note_lines: list[str] = [line.strip() for line in note.split('\n')]
        item_line, op_line, test_line, true_line, false_line = note_lines[1:]

        self.inspection_count: int = 0

        self.held_items: list[int] = []
        if item_line.startswith('Starting items:'):
            self.held_items = [int(n) for n in item_line.split(':')[1].split(',')]
        else:
            print('Bad starting held_items line')

        self.operation: str = ''
        if op_line.startswith('Operation:'):
            self.operation = op_line.split('=')[1].strip()
        else:
            print('Bad operation line')

        self.test: int = 1
        if test_line.startswith('Test:'):
            self.test = int(test_line.split()[-1])
        else:
            print('Bad test line')

        self.true_toss: int = 1
        if true_line.startswith('If true:'):
            self.true_toss = int(true_line.split()[-1])
        else:
            print('Bad true line')

        self.false_toss: int = 1
        if false_line.startswith('If false:'):
            self.false_toss = int(false_line.split()[-1])
        else:
            print('Bad false line')

    def perform_operation(self, cur_level: int) -> int:
        val1, op, val2 = self.operation.split()
        val1 = cur_level if val1 == 'old' else int(val1)
        val2 = cur_level if val2 == 'old' else int(val2)

        match op:
            case '+':
                return val1 + val2
            case '*':
                return val1 * val2
            case _:
                return cur_level

    def take_turn(self, worry_factor: int = 1) -> dict[int, list[int]]:
        tossed_items: defaultdict[int, list[int]] = defaultdict(list)

        for worry_level in self.held_items:
            self.inspection_count += 1
            worry_level: int = self.perform_operation(worry_level) // worry_factor

            toss_target: int = self.true_toss if worry_level % self.test == 0 else self.false_toss
            tossed_items[toss_target].append(worry_level)

        self.held_items.clear()

        return tossed_items


def parse(puzzle_input):
    """Parse input"""
    return [Monkey(m) for m in puzzle_input.split('\n\n')]


def get_reduction_factor(monkeys: list[Monkey]) -> int:
    factor: int = 1
    for monkey in monkeys:
        factor *= monkey.test
    return factor


def print_monkeys(monkeys: list[Monkey]) -> None:
    for i, monkey in enumerate(monkeys):
        print(f'Monkey {i}: ' + ', '.join(str(item) for item in monkey.held_items))
    print()


def part1(data):
    """Solve part 1"""
    reduction_factor: int = get_reduction_factor(data)

    rounds: int = 20
    for _ in range(rounds):
        for monkey in data:
            tosses: dict[int, list[int]] = monkey.take_turn(worry_factor=3)
            for target, new_items in tosses.items():
                new_items = [item % reduction_factor for item in new_items]
                data[target].held_items.extend(new_items)

        # print_monkeys(data)

    inspection_counts: list[int] = sorted(monkey.inspection_count for monkey in data)

    return inspection_counts[-1] * inspection_counts[-2]


def part2(data):
    """Solve part 2"""
    reduction_factor: int = get_reduction_factor(data)

    rounds: int = 10000
    for _ in range(rounds):
        for monkey in data:
            tosses: dict[int, list[int]] = monkey.take_turn()
            for target, new_items in tosses.items():
                new_items = [item % reduction_factor for item in new_items]
                data[target].held_items.extend(new_items)

        # print_monkeys(data)

    inspection_counts: list[int] = sorted(monkey.inspection_count for monkey in data)

    return inspection_counts[-1] * inspection_counts[-2]


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
