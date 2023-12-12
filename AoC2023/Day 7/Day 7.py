import pathlib
import sys
import os
from typing import Iterable


class Hand:
    CARDS: str = '23456789TJQKA'

    Type = int
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __init__(self, hand: str) -> None:
        self.hand: str = hand
        self.count: dict[str, int] = {card: hand.count(card) for card in hand}

    def __repr__(self) -> str:
        s: str = ''
        for card in self.CARDS:
            if card in self.hand:
                s += card * self.count[card]
        return s

    def __lt__(self, other: 'Hand') -> bool:
        if self.type() == other.type():
            for self_card, other_card in zip(self.hand, other.hand):
                if self_card != other_card:
                    return self.CARDS.index(self_card) < self.CARDS.index(other_card)
        return self.type() < other.type()

    def type(self) -> Type:
        if len(self.count) == 1:
            return Hand.FIVE_OF_A_KIND
        if 4 in self.count.values():
            return Hand.FOUR_OF_A_KIND
        if len(self.count) == 2:
            return Hand.FULL_HOUSE
        if 3 in self.count.values():
            return Hand.THREE_OF_A_KIND
        if len(self.count) == 3:
            return Hand.TWO_PAIR
        if len(self.count) == 4:
            return Hand.ONE_PAIR
        return Hand.HIGH_CARD


class JokerHand(Hand):
    CARDS: str = 'J23456789TQKA'

    # Return best possible type using jokers
    def type(self) -> Hand.Type:
        jokers: int = self.count.get('J', 0)
        non_jokers: dict[str, int] = {card: num for card, num in self.count.items() if card != 'J'}

        if len(non_jokers) <= 1:  # J <= 5
            return Hand.FIVE_OF_A_KIND
        if 4 - jokers in non_jokers.values():  # J <= 3
            return Hand.FOUR_OF_A_KIND
        if len(non_jokers) == 2:  # J <= 1
            return Hand.FULL_HOUSE
        if 3 - jokers in non_jokers.values():  # J <= 2
            return Hand.THREE_OF_A_KIND
        if len(non_jokers) == 3:  # J <= 1
            return Hand.TWO_PAIR
        if len(non_jokers) == 4:  # J <= 1
            return Hand.ONE_PAIR
        return Hand.HIGH_CARD  # J = 0


def parse(puzzle_input):
    """Parse input"""
    hands: list[tuple[Hand, int]] = []
    for line in puzzle_input.split('\n'):
        hand, bid = line.split()
        hands.append((Hand(hand), int(bid)))
    return hands


def total_winnings(hands: Iterable[tuple[Hand, int]]) -> int:
    return sum(rank * bid for rank, (_, bid) in enumerate(sorted(hands), 1))


def part1(data):
    """Solve part 1"""
    return total_winnings(data)


def part2(data):
    """Solve part 2"""
    return total_winnings((JokerHand(h.hand), bid) for h, bid in data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 6440
    PART2_TEST_ANSWER = 5905

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
