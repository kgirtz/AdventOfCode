import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    responses: list[list[str]] = []
    for group in puzzle_input.split('\n\n'):
        responses.append(group.split())
    return responses


def all_group_yeses(responses: list[list[str]]) -> list[set[str]]:
    affirmatives: list[set[str]] = []
    for group in responses:
        cur_set: set[str] = set()
        for response in group:
            cur_set.update(response)
        affirmatives.append(cur_set)
    return affirmatives


def common_group_yeses(responses: list[list[str]]) -> list[set[str]]:
    affirmatives: list[set[str]] = []
    for group in responses:
        cur_set: set[str] = set(group[0])
        for response in group[1:]:
            cur_set &= set(response)
        affirmatives.append(cur_set)
    return affirmatives


def part1(data):
    """Solve part 1"""
    return sum(len(questions) for questions in all_group_yeses(data))


def part2(data):
    """Solve part 2"""
    return sum(len(questions) for questions in common_group_yeses(data))


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
