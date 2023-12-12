import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def parse_expression(expr: str) -> list[str]:
    elements: list[str] = []
    parens: list[int] = []
    for i, element in enumerate(expr):
        if element == ' ':
            continue

        if not parens and element not in '()':
            elements.append(element)
            continue

        if element == '(':
            parens.append(i)
        elif element == ')':
            open_paren: int = parens.pop()
            if not parens:
                elements.append(expr[open_paren + 1:i])

    return elements


def evaluate_no_precedence(expression: str) -> int:
    if expression.isdigit():
        return int(expression)

    results: list[str] = parse_expression(expression)

    result: int = evaluate_no_precedence(results[0])
    op: str = '+'
    for element in results[1:]:
        if element in '+*':
            op = element
        elif op == '+':
            result += evaluate_no_precedence(element)
        elif op == '*':
            result *= evaluate_no_precedence(element)
    return result


def evaluate_plus_precedence(expression: str) -> int:
    if expression.isdigit():
        return int(expression)

    results: list[str] = parse_expression(expression)

    i: int = 0
    while i < len(results) - 1:
        if results[i + 1] == '+':
            a: int = evaluate_plus_precedence(results[i])
            b: int = evaluate_plus_precedence(results[i + 2])
            results[i:i + 3] = [str(a + b)]
        else:
            i += 1

    result: int = 1
    for element in results[::2]:
        result *= evaluate_plus_precedence(element)
    return result


def part1(data):
    """Solve part 1"""
    total: int = 0
    for expression in data:
        total += evaluate_no_precedence(expression)
    return total


def part2(data):
    """Solve part 2"""
    total: int = 0
    for expression in data:
        total += evaluate_plus_precedence(expression)
    return total


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
