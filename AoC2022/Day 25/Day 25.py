import pathlib
import sys
import os

SNAFU_TO_DEC: dict[str, int] = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
DEC_TO_SNAFU: dict[int, str] = {0: '0', 1: '1', 2: '2', 3: '1=', 4: '1-', -1: '-', -2: '='}


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split('\n')


def add_SNAFU(a: str, b: str) -> str:
    a = a[::-1]
    b = b[::-1]

    if len(a) < len(b):
        a += '0' * (len(b) - len(a))
    if len(b) < len(a):
        b += '0' * (len(a) - len(b))

    sumfu: str = ''
    carry: int = 0

    for i in range(len(a)):
        snigit_sum: int = SNAFU_TO_DEC[a[i]] + SNAFU_TO_DEC[b[i]] + carry
        match snigit_sum:
            case 4:
                carry = 1
                sumfu += '-'
            case 3:
                carry = 1
                sumfu += '='
            case _:
                carry = 0
                sumfu += DEC_TO_SNAFU[snigit_sum]

    if carry != 0:
        sumfu += DEC_TO_SNAFU[carry]

    return sumfu[::-1]


def to_SNAFU(n: int) -> str:
    s: str = '0'
    power: int = 0
    while n != 0:
        s = add_SNAFU(s, DEC_TO_SNAFU[n % 5] + '0' * power)
        n //= 5
        power += 1
    return s


def from_SNAFU(s: str) -> int:
    n: int = 0
    power: int = 1
    for snigit in s[::-1]:
        n += SNAFU_TO_DEC[snigit] * power
        power *= 5
    return n


def part1(data):
    """Solve part 1"""

    return to_SNAFU(sum(from_SNAFU(s) for s in data))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
