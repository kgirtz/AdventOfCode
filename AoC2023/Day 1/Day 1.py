import pathlib
import sys
import os


DIGIT_WORDS: dict[str, str] = {'one': '1',
                                 'two': '2',
                                 'three': '3',
                                 'four': '4',
                                 'five': '5',
                                 'six': '6',
                                 'seven': '7',
                                 'eight': '8',
                                 'nine': '9'}
DIGIT_WORDS_REV: dict[str, str] = {word[::-1]: digit for word, digit in DIGIT_WORDS.items()}


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split('\n')


def calibration_value(line: str, *, include_words: bool = False) -> int:
    value: str = ''
    for i, ch in enumerate(line):
        if ch.isdigit():
            value += ch
        elif include_words:
            for word, digit in DIGIT_WORDS.items():
                if line[i:].startswith(word):
                    value += digit
                    break
        if len(value) == 1:
            break

    enil: str = line[::-1]
    for i, ch in enumerate(enil):
        if ch.isdigit():
            value += ch
        elif include_words:
            for word, digit in DIGIT_WORDS_REV.items():
                if enil[i:].startswith(word):
                    value += digit
                    break
        if len(value) == 2:
            break

    return int(value)


def part1(data):
    """Solve part 1"""
    return sum(calibration_value(line) for line in data)


def part2(data):
    """Solve part 2"""
    return sum(calibration_value(line, include_words=True) for line in data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 142
    PART2_TEST_ANSWER = 281

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
