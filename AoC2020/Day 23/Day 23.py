import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(label) for label in puzzle_input.strip()]


class CupCircle:
    def __init__(self, labels: list[int], max_label: int = 0) -> None:
        self.min_label: int = min(labels)
        self.max_label: int = max(labels) if max_label == 0 else max_label
        self.cur_cup: int = labels[0]
        self.next: dict[int, int] = {labels[i]: labels[i + 1] for i in range(len(labels) - 1)}
        if max_label > max(labels):
            cur: int = labels[-1]
            for label in range(max(labels) + 1, max_label + 1):
                self.next[cur] = label
                cur = label
            self.next[cur] = labels[0]
        else:
            self.next[labels[-1]] = labels[0]

    def list_of_labels(self) -> list[int]:
        labels: list[int] = [self.cur_cup]
        cur: int = self.next[self.cur_cup]
        while cur != self.cur_cup:
            labels.append(cur)
            cur = self.next[cur]
        return labels

    def move(self) -> None:
        first_picked_up: int = self.next[self.cur_cup]
        last_picked_up: int = self.next[self.next[first_picked_up]]
        picked_up: set[int] = {first_picked_up, self.next[first_picked_up], last_picked_up}

        self.next[self.cur_cup] = self.next[last_picked_up]

        destination: int = self.cur_cup - 1
        if destination < self.min_label:
            destination = self.max_label
        while destination in picked_up:
            destination -= 1
            if destination < self.min_label:
                destination = self.max_label

        self.next[last_picked_up] = self.next[destination]
        self.next[destination] = first_picked_up

        self.cur_cup = self.next[self.cur_cup]


def part1(data):
    """Solve part 1"""
    circle: CupCircle = CupCircle(data)
    for _ in range(100):
        circle.move()

    circle.cur_cup = 1
    labels: list[int] = circle.list_of_labels()
    return ''.join(str(label) for label in labels[1:])


def part2(data):
    """Solve part 2"""
    circle: CupCircle = CupCircle(data, max_label=1000000)
    for i in range(10000000):
        circle.move()

    circle.cur_cup = 1
    circle.cur_cup = circle.next[circle.cur_cup]
    return circle.cur_cup * circle.next[circle.cur_cup]


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
        puzzle_input = pathlib.Path('./' + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
