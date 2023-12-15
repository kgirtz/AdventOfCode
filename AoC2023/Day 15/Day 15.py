import pathlib
import sys
import os
import dataclasses


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split(',')


def hash_algorithm(characters: str) -> int:
    value: int = 0
    for ch in characters:
        value = 17 * (value + ord(ch)) % 256
    return value


@dataclasses.dataclass
class Lens:
    label: str
    focal_length: int


@dataclasses.dataclass
class Box:
    lenses: list[Lens] = dataclasses.field(default_factory=list)

    def remove(self, label: str) -> None:
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                self.lenses.remove(lens)
                return

    def add(self, new_lens: Lens) -> None:
        for i, lens in enumerate(self.lenses):
            if lens.label == new_lens.label:
                self.lenses[i] = new_lens
                return
        self.lenses.append(new_lens)


def part1(data):
    """Solve part 1"""
    return sum(hash_algorithm(step) for step in data)


def part2(data):
    """Solve part 2"""
    boxes: list[Box] = [Box() for _ in range(256)]
    for step in data:
        label: str = step.split('=')[0].rstrip('-')
        box: Box = boxes[hash_algorithm(label)]
        if '-' in step:
            box.remove(label)
        else:
            focal_length: int = int(step.split('=')[1])
            box.add(Lens(label, focal_length))

    focusing_power: int = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box.lenses):
            focusing_power += (i + 1) * (j + 1) * lens.focal_length

    return focusing_power


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 1320
    PART2_TEST_ANSWER = 145

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
