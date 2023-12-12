import pathlib
import sys
import os
import dataclasses


@dataclasses.dataclass
class Card:
    winning_numbers: set[int]
    my_numbers: set[int]

    def num_matches(self) -> int:
        return len(self.winning_numbers & self.my_numbers)

    def value(self) -> int:
        matches: int = self.num_matches()
        return pow(2, matches - 1) if matches > 0 else 0


def parse(puzzle_input):
    """Parse input"""
    cards: list[Card] = []
    for line in puzzle_input.split('\n'):
        nums: str = line.split(':')[1]
        winning: set[int] = {int(num) for num in nums.split('|')[0].strip().split()}
        have: set[int] = {int(num) for num in nums.split('|')[1].strip().split()}
        cards.append(Card(winning, have))
    return cards


def payout(cards: list[Card]) -> list[int]:
    card_counts: list[int] = [1] * len(cards)
    for i, card in enumerate(cards):
        for j in range(card.num_matches()):
            card_counts[i + j + 1] += card_counts[i]
    return card_counts


def part1(data):
    """Solve part 1"""
    return sum(card.value() for card in data)


def part2(data):
    """Solve part 2"""
    return sum(payout(data))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 13
    PART2_TEST_ANSWER = 30

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
