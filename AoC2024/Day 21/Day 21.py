import pathlib
import sys
import os
import collections

from space import Space
from xypair import XYpair


class Keypad(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        # all keys are unique so simplify self.items to self.position
        self.position: dict[str, XYpair] = {key: self.initial_position(key) for key in self.items}
        self.gap: XYpair = self.position[' ']

    def shortest_paths_to_key(self, start_key: str, finish_key: str) -> list[str]:
        start: XYpair = self.position[start_key]
        finish: XYpair = self.position[finish_key]
        diff: XYpair = finish - start

        horizontal_steps: str = ''
        if diff.x > 0:
            horizontal_steps = '>' * diff.x
        elif diff.x < 0:
            horizontal_steps = '<' * -diff.x

        vertical_steps: str = ''
        if diff.y > 0:
            vertical_steps = 'v' * diff.y
        elif diff.y < 0:
            vertical_steps = '^' * -diff.y

        if not horizontal_steps or not vertical_steps:
            return [horizontal_steps + vertical_steps]
        if (finish.x, start.y) == self.gap:
            return [vertical_steps + horizontal_steps]
        if (start.x, finish.y) == self.gap:
            return [horizontal_steps + vertical_steps]
        return [horizontal_steps + vertical_steps, vertical_steps + horizontal_steps]

    def shortest_sequences(self, keys_to_press: str) -> list[str]:
        paths: list[str] = ['']
        cur_key: str = 'A'
        for key in keys_to_press:
            new_paths: list[str] = []
            for path in self.shortest_paths_to_key(cur_key, key):
                new_paths.extend(f'{p}{path}A' for p in paths)
            paths = new_paths
            cur_key = key

        min_length: int = min(len(path) for path in paths)
        return [path for path in paths if len(path) == min_length]

    def shortest_sequence_fast(self, keys_to_press: dict[str, int]) -> dict[str, int]:
        sequence: dict[str, int] = collections.defaultdict(int)
        for sub_seq, num in keys_to_press.items():
            cur_key: str = 'A'
            for key in sub_seq:
                for path in self.shortest_paths_to_key(cur_key, key):
                    sequence[path + 'A'] += num
                cur_key = key
        return sequence


class DirectionKeypad(Keypad):
    def shortest_paths_to_key(self, start_key: str, finish_key: str) -> list[str]:
        if start_key == finish_key:
            return ['']

        if start_key == 'A':
            if finish_key == '^':
                return ['<']
            elif finish_key == 'v':
                return ['<v']  # swap?
            elif finish_key == '<':
                return ['v<<']
            elif finish_key == '>':
                return ['v']
        elif start_key == '^':
            if finish_key == 'A':
                return ['>']
            elif finish_key == 'v':
                return ['v']
            elif finish_key == '<':
                return ['v<']
            elif finish_key == '>':
                return ['v>']  # swap?
        elif start_key == 'v':
            if finish_key == 'A':
                return ['^>']  # swap?
            elif finish_key == '^':
                return ['^']
            elif finish_key == '<':
                return ['<']
            elif finish_key == '>':
                return ['>']
        elif start_key == '<':
            if finish_key == 'A':
                return ['>>^']
            elif finish_key == '^':
                return ['>^']
            elif finish_key == 'v':
                return ['>']
            elif finish_key == '>':
                return ['>>']
        elif start_key == '>':
            if finish_key == 'A':
                return ['^']
            elif finish_key == '^':
                return ['<^']  # swap?
            elif finish_key == 'v':
                return ['<']
            elif finish_key == '<':
                return ['<<']


numeric_layout: list[str] = ['789',
                             '456',
                             '123',
                             ' 0A']
numeric_keypad: Keypad = Keypad(numeric_layout)

direction_layout: list[str] = [' ^A',
                               '<v>']
direction_keypad: DirectionKeypad = DirectionKeypad(direction_layout)


def len_shortest_sequence(code: str, num_robots: int) -> int:
    # Shortest sequences for code on keypad
    sequences: list[str] = numeric_keypad.shortest_sequences(code)

    for _ in range(num_robots):
        # Shortest sequences for above on direction pad
        new_sequences: list[str] = []
        for s in sequences:
            new_sequences.extend(direction_keypad.shortest_sequences(s))
        min_length: int = min(len(s) for s in new_sequences)
        sequences = [s for s in new_sequences if len(s) == min_length]

    return min(len(s) for s in sequences)


def len_shortest_sequence_fast(code: str, num_robots: int) -> int:
    # Shortest sequences for code on keypad
    sequences: list[str] = numeric_keypad.shortest_sequences(code)

    min_length: int = -1
    for sequence in sequences:
        # Build dictionary
        s_dict: dict[str, int] = collections.defaultdict(int)
        for s in sequence.replace('A', 'A,').split(',')[:-1]:
            s_dict[s] += 1

        for _ in range(num_robots):
            s_dict = direction_keypad.shortest_sequence_fast(s_dict)

        final_length: int = sum(len(k) * v for k, v in s_dict.items())
        if final_length < min_length or min_length == -1:
            min_length = final_length

    return min_length


def complexity(code: str, num_robots: int) -> int:
    return int(code.rstrip('A')) * len_shortest_sequence_fast(code, num_robots)


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.split('\n')


def part1(data):
    """Solve part 1"""
    return sum(complexity(code, 2) for code in data)


def part2(data):
    """Solve part 2"""  # 395617529305636 is too high
    return sum(complexity(code, 25) for code in data)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 126384
    PART2_TEST_ANSWER = None

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
