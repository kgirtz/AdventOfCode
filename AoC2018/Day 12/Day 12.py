import pathlib
import sys
import os
from collections.abc import Sequence


def pots_to_int(pots: str) -> int:
    num: int = 0
    for i, pot in enumerate(pots):
        if pot == '#':
            num |= (1 << i)
    return num


def parse(puzzle_input: str):
    """Parse input"""
    initial_state_str, rules_str = puzzle_input.split('\n\n')

    initial_state: int = pots_to_int(initial_state_str.split()[-1])

    rules: list[bool] = [False] * pow(2, 5)
    for line in rules_str.split('\n'):
        pattern, result = line.split(' => ')
        if result == '#':
            rules[pots_to_int(pattern)] = True

    return initial_state, tuple(rules)


def generation(pots: int, lsb_position: int, rules: Sequence[bool]) -> (int, int):
    # Assume LSB is always 1
    lsb_position -= 2
    pots <<= 2

    cur_pot: int = 0
    new_pots: int = 0
    pots <<= 2
    while pots:
        surrounding: int = pots & 0b11111
        if rules[surrounding]:
            new_pots |= (1 << cur_pot)
        cur_pot += 1
        pots >>= 1

    while (new_pots & 1) == 0:
        new_pots >>= 1
        lsb_position += 1
    return new_pots, lsb_position


def sum_of_pots(pots: int, lsb_position: int) -> int:
    total: int = 0
    bit: int = lsb_position
    while pots:
        if pots & 1:
            total += bit
        bit += 1
        pots >>= 1
    return total


def fast_forward(generations: int, pots: int, lsb_position: int, rules: Sequence[bool]) -> (int, int):
    seen: dict[int, tuple[int, int]] = {}
    for g in range(generations):
        seen[pots] = (g, lsb_position)

        pots, lsb_position = generation(pots, lsb_position, rules)

        if pots in seen:
            startup, init_lsb_position = seen[pots]

            cycle_length: int = g - startup + 1
            cycle_shift: int = lsb_position - init_lsb_position
            num_cycles: int = (generations - startup) // cycle_length

            reduced_generations: int = (generations - startup) % cycle_length
            new_lsb_position: int = num_cycles * cycle_shift + init_lsb_position
            return fast_forward(reduced_generations, pots, new_lsb_position, rules)

    return pots, lsb_position


def part1(data):
    """Solve part 1"""
    initial_state, rules = data
    pots, lsb_position = fast_forward(20, initial_state, 0, rules)
    return sum_of_pots(pots, lsb_position)


def part2(data):
    """Solve part 2"""
    initial_state, rules = data
    pots, lsb_position = fast_forward(50000000000, initial_state, 0, rules)
    return sum_of_pots(pots, lsb_position)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 325
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
