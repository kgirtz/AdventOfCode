import pathlib
import sys
import os
from typing import Sequence


def parse(puzzle_input):
    """Parse input"""
    tech_list: list[tuple[str, int]] = []
    for technique in puzzle_input.split('\n'):
        if technique == 'deal into new stack':
            tech_list.append(('s', 0))
        elif technique.startswith('deal with increment '):
            increment: int = int(technique.split()[-1])
            tech_list.append(('i', increment))
        elif technique.startswith('cut '):
            amount: int = int(technique.split()[-1])
            tech_list.append(('c', amount))
    return tech_list


def modulus_divide(a: int, b: int, m: int) -> int:
    while a % b != 0:
        a += m
    return a // b


def compress_technique_list(techniques: Sequence[str], deck_len: int) -> tuple[int, int]:
    a: int = 1
    b: int = 0
    for technique, amount in techniques:
        match technique:
            case 's':
                a = -a % deck_len
                b = -(b + 1) % deck_len
            case 'i':
                a = (a * amount) % deck_len
                b = (b * amount) % deck_len
            case 'c':
                b = (b - amount) % deck_len
    return a, b


def compress_technique_undo_list(techniques: Sequence[str], deck_len: int) -> tuple[int, int]:
    a: int = 1
    b: int = 0
    for technique, amount in list(reversed(techniques)):
        match technique:
            case 's':
                a = -a % deck_len
                b = -(b + 1) % deck_len
            case 'i':
                a = modulus_divide(a, amount, deck_len)
                b = modulus_divide(b, amount, deck_len)
            case 'c':
                b = (b + amount) % deck_len
    return a, b


def compress_repeated_operations(a: int, b: int, iterations: int, deck_len: int) -> tuple[int, int]:
    new_a: int = a
    new_b: int = b
    for _ in range(iterations - 1):
        new_a = (a * new_a) % deck_len
        new_b = (a * new_b + b) % deck_len
    return new_a, new_b


def apply_compressed_shuffle_to_pos(pos: int, a: int, b: int, deck_len: int, iterations: int = 1) -> int:
    for _ in range(iterations):
        pos = (a * pos + b) % deck_len
    return pos


def apply_techniques(pos: int, techniques: Sequence[str], deck_len: int, iterations: int = 1) -> int:
    a, b = compress_technique_list(techniques, deck_len)
    a, b = compress_repeated_operations(a, b, iterations, deck_len)
    return apply_compressed_shuffle_to_pos(pos, a, b, deck_len)


def undo_techniques(pos: int, techniques: Sequence[str], deck_len: int, iterations: int = 1) -> int:
    a, b = compress_technique_undo_list(techniques, deck_len)

    powers_of_ten_operations: list[tuple[int, int]] = []
    dividend: int = iterations
    while dividend:
        powers_of_ten_operations.append((a, b))
        a, b = compress_repeated_operations(a, b, 10, deck_len)
        dividend //= 10

    for a, b in powers_of_ten_operations:
        pos = apply_compressed_shuffle_to_pos(pos, a, b, deck_len, iterations % 10)
        iterations //= 10

    return pos


def part1(data):
    """Solve part 1"""
    return apply_techniques(pos=2019, techniques=data, deck_len=10007)


def part2(data):
    """Solve part 2"""
    return undo_techniques(pos=2020, techniques=data, deck_len=119315717514047, iterations=101741582076661)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
