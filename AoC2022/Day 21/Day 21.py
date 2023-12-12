import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    monkeys: dict[str, str] = {}
    for line in puzzle_input.split('\n'):
        name, job = line.split(':')
        monkeys[name] = job.strip()
    return monkeys


def yelled_by_monkey(name: str, monkeys: dict[str, str]) -> int | str:
    job: str = monkeys[name]

    # Leaf, unknown
    if job == '???':
        return job

    # Leaf, just a number
    if len(job.split()) == 1:
        return int(job)

    # Internal node, evaluate children
    l_child, op, r_child = job.split()
    l_num: int | str = yelled_by_monkey(l_child, monkeys)
    r_num: int | str = yelled_by_monkey(r_child, monkeys)

    if type(l_num) is int and type(r_num) is int:
        match op:
            case '+':
                return l_num + r_num
            case '-':
                return l_num - r_num
            case '*':
                return l_num * r_num
            case '/':
                return l_num // r_num
    else:
        if op == '=':
            return f'{l_num} {op} {r_num}'
        else:
            return f'({l_num} {op} {r_num})'


def monkey_in_subtree(name: str, root: str, tree: dict[str, str]) -> bool:
    if root == name:
        return True
    if len(tree[root].split()) == 1:
        return False

    l_child, _, r_child = tree[root].split()
    return monkey_in_subtree(name, l_child, tree) or monkey_in_subtree(name, r_child, tree)


def solve_for_humn(root_value: int, root: str, tree: dict[str, str]) -> None:
    if root == 'humn':
        tree['humn'] = str(root_value)
        return

    l_tree, op, r_tree = tree[root].split()
    if monkey_in_subtree('humn', l_tree, tree):
        r_value: int = yelled_by_monkey(r_tree, tree)
        match op:
            case '+':
                solve_for_humn(root_value - r_value, l_tree, tree)
            case '-':
                solve_for_humn(root_value + r_value, l_tree, tree)
            case '*':
                solve_for_humn(root_value // r_value, l_tree, tree)
            case '/':
                solve_for_humn(root_value * r_value, l_tree, tree)
    else:
        l_value: int = yelled_by_monkey(l_tree, tree)
        match op:
            case '+':
                solve_for_humn(root_value - l_value, r_tree, tree)
            case '-':
                solve_for_humn(l_value - root_value, r_tree, tree)
            case '*':
                solve_for_humn(root_value // l_value, r_tree, tree)
            case '/':
                solve_for_humn(l_value // root_value, r_tree, tree)


def part1(data):
    """Solve part 1"""

    return yelled_by_monkey('root', data)


def part2(data):
    """Solve part 2"""
    data['root'] = data['root'].replace('+', '=')
    data['humn'] = '???'

    l_tree, _, r_tree = data['root'].split()
    if monkey_in_subtree('humn', l_tree, data):
        total: int = yelled_by_monkey(r_tree, data)
        solve_for_humn(total, l_tree, data)
    else:
        total: int = yelled_by_monkey(l_tree, data)
        solve_for_humn(total, r_tree, data)

    return yelled_by_monkey('humn', data)


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
