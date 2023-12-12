import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    data = []
    for line in puzzle_input.split('\n'):
        segments, digits = line.split('|')
        data.append((segments.split(), digits.split()))
    return data


def generate_mapping(signals: list[str]) -> dict[int, set[str]]:
    mapping: dict[int, set] = {}
    finished: set[str] = set(mapping.values())

    for signal in signals:
        if len(signal) == 2:
            mapping[1] = set(signal)
            finished.add(signal)
        elif len(signal) == 4:
            mapping[4] = set(signal)
            finished.add(signal)
        elif len(signal) == 3:
            mapping[7] = set(signal)
            finished.add(signal)
        elif len(signal) == 7:
            mapping[8] = set(signal)
            finished.add(signal)

    bd: set[str] = mapping[4] - mapping[1]
    for signal in set(signals) - finished:
        sig_set: set[str] = set(signal)
        if len(signal) == 5 and sig_set & bd == bd:
            mapping[5] = sig_set
            finished.add(signal)

    ce: set[str] = mapping[8] - mapping[5]
    for signal in set(signals) - finished:
        sig_set = set(signal)
        if len(sig_set) == 6 and sig_set & ce == ce:
            mapping[0] = sig_set
            finished.add(signal)
        elif len(sig_set) == 5 and sig_set & ce == ce:
            mapping[2] = sig_set
            finished.add(signal)
        elif sig_set == mapping[5] | mapping[1]:
            mapping[9] = sig_set
            finished.add(signal)

    for signal in set(signals) - finished:
        sig_set = set(signal)
        if len(sig_set) == 5:
            mapping[3] = sig_set
        else:
            mapping[6] = sig_set

    return mapping


def get_digit(signal: str, mapping: dict[int, set[str]]) -> int:
    signal_set: set[str] = set(signal)
    for digit, sig_set in mapping.items():
        if signal_set == sig_set:
            return digit


def part1(data):
    """Solve part 1"""
    unique_digits: int = 0
    for signals, output in data:
        cur_map: dict[int, set[str]] = generate_mapping(signals)
        for digit_sig in output:
            if get_digit(digit_sig, cur_map) in (1, 4, 7, 8):
                unique_digits += 1
    return unique_digits


def part2(data):
    """Solve part 2"""
    total: int = 0
    for signals, output in data:
        cur_map: dict[int, set[str]] = generate_mapping(signals)
        digits: list[str] = [str(get_digit(d, cur_map)) for d in output]
        total += int(''.join(digits))
    return total


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
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
