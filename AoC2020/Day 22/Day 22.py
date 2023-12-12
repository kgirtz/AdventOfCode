import pathlib
import sys
import os
from collections import deque


def parse(puzzle_input):
    """Parse input"""
    p1_str, p2_str = puzzle_input.split('\n\n')
    p1 = [int(card) for card in p1_str.split('\n')[1:]]
    p2 = [int(card) for card in p2_str.split('\n')[1:]]
    return p1, p2


def combat(p1_list: list[int], p2_list: list[int]) -> list[int]:
    p1: deque[int] = deque(p1_list)
    p2: deque[int] = deque(p2_list)

    while p1 and p2:
        p1_card: int = p1.popleft()
        p2_card: int = p2.popleft()
        if p1_card > p2_card:
            p1.extend((p1_card, p2_card))
        else:
            p2.extend((p2_card, p1_card))

    if p1:
        return list(p1)
    else:
        return list(p2)


def recursive_combat(p1_list: list[int], p2_list: list[int]) -> list[int]:

    def sub_game(p1_sublist: list[int], p2_sublist: list[int]) -> tuple[int, list[int]]:
        p1: deque[int] = deque(p1_sublist)
        p2: deque[int] = deque(p2_sublist)
        states: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()

        while p1 and p2:
            if (tuple(p1), tuple(p2)) in states:
                return 1, list(p1)
            states.add((tuple(p1), tuple(p2)))

            p1_card: int = p1.popleft()
            p2_card: int = p2.popleft()

            if len(p1) >= p1_card and len(p2) >= p2_card:
                winner, _ = sub_game(list(p1)[:p1_card], list(p2)[:p2_card])
                if winner == 1:
                    p1.extend((p1_card, p2_card))
                else:
                    p2.extend((p2_card, p1_card))
            else:
                if p1_card > p2_card:
                    p1.extend((p1_card, p2_card))
                else:
                    p2.extend((p2_card, p1_card))

        if p1:
            return 1, list(p1)
        else:
            return 2, list(p2)

    _, deck = sub_game(p1_list, p2_list)
    return deck


def score(deck: list[int]) -> int:
    total: int = 0
    for i, value in enumerate(reversed(deck), 1):
        total += value * i
    return total


def part1(data):
    """Solve part 1"""
    p1_deck, p2_deck = data
    winning_deck: list[int] = combat(p1_deck, p2_deck)
    return score(winning_deck)


def part2(data):
    """Solve part 2"""
    p1_deck, p2_deck = data
    winning_deck: list[int] = recursive_combat(p1_deck, p2_deck)
    return score(winning_deck)


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
