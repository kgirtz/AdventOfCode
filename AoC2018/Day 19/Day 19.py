import pathlib
import sys
import os
from collections.abc import Sequence
from typing import TypeAlias

Instruction: TypeAlias = tuple[str, int, int, int]


class Device:
    def __init__(self, ip_register: int) -> None:
        self.registers: list[int] = [0, 0, 0, 0, 0, 0]
        self.ip_register: int = ip_register
        self.ip: int = 0

    def execute(self, instruction: Instruction) -> None:
        if self.ip_register != -1:
            self.registers[self.ip_register] = self.ip

        opcode, a, b, c = instruction

        match opcode:
            case 'addr':
                self.registers[c] = self.registers[a] + self.registers[b]
            case 'addi':
                self.registers[c] = self.registers[a] + b
            case 'mulr':
                self.registers[c] = self.registers[a] * self.registers[b]
            case 'muli':
                self.registers[c] = self.registers[a] * b
            case 'banr':
                self.registers[c] = self.registers[a] & self.registers[b]
            case 'bani':
                self.registers[c] = self.registers[a] & b
            case 'borr':
                self.registers[c] = self.registers[a] | self.registers[b]
            case 'bori':
                self.registers[c] = self.registers[a] | b
            case 'setr':
                self.registers[c] = self.registers[a]
            case 'seti':
                self.registers[c] = a
            case 'gtir':
                self.registers[c] = 1 if a > self.registers[b] else 0
            case 'gtri':
                self.registers[c] = 1 if self.registers[a] > b else 0
            case 'gtrr':
                self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0
            case 'eqir':
                self.registers[c] = 1 if a == self.registers[b] else 0
            case 'eqri':
                self.registers[c] = 1 if self.registers[a] == b else 0
            case 'eqrr':
                self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

        if self.ip_register != -1:
            self.ip = self.registers[self.ip_register]

    def run(self, program: Sequence[Instruction]) -> None:
        self.ip = 0
        while 0 <= self.ip < len(program):
            next_instruction: Instruction = program[self.ip]
            self.execute(next_instruction)
            self.ip += 1

    def decompile(self, instruction: Instruction) -> str:
        opcode, a, b, c = instruction

        s: str = ''
        match opcode:
            case 'addr':
                if c == a:
                    s = f'r[{c}] += r[{b}]'
                elif c == b:
                    s = f'r[{c}] += r[{a}]'
                else:
                    s = f'r[{c}] = r[{a}] + r[{b}]'
            case 'addi':
                if c == a:
                    s = f'r[{c}] += {b}'
                else:
                    s = f'r[{c}] = r[{a}] + {b}'
            case 'mulr':
                if c == a:
                    s = f'r[{c}] *= r[{b}]'
                elif c == b:
                    s = f'r[{c}] *= r[{a}]'
                else:
                    s = f'r[{c}] = r[{a}] * r[{b}]'
            case 'muli':
                if c == a:
                    s = f'r[{c}] *= {b}'
                else:
                    s = f'r[{c}] = r[{a}] * {b}'
            case 'banr':
                if c == a:
                    s = f'r[{c}] &= r[{b}]'
                elif c == b:
                    s = f'r[{c}] &= r[{a}]'
                else:
                    s = f'r[{c}] = r[{a}] & r[{b}]'
            case 'bani':
                if c == a:
                    s = f'r[{c}] &= {b}'
                else:
                    s = f'r[{c}] = r[{a}] & {b}'
            case 'borr':
                if c == a:
                    s = f'r[{c}] |= r[{b}]'
                elif c == b:
                    s = f'r[{c}] |= r[{a}]'
                else:
                    s = f'r[{c}] = r[{a}] | r[{b}]'
            case 'bori':
                if c == a:
                    s = f'r[{c}] |= {b}'
                else:
                    s = f'r[{c}] = r[{a}] | {b}'
            case 'setr':
                s = f'r[{c}] = r[{a}]'
            case 'seti':
                s = f'r[{c}] = {a}'
            case 'gtir':
                s = f'r[{c}] = ({a} > r[{b}])'
            case 'gtri':
                s = f'r[{c}] = (r[{a}] > {b})'
            case 'gtrr':
                s = f'r[{c}] = (r[{a}] > r[{b}])'
            case 'eqir':
                s = f'r[{c}] = ({a} == r[{b}])'
            case 'eqri':
                s = f'r[{c}] = (r[{a}] == {b})'
            case 'eqrr':
                s = f'r[{c}] = (r[{a}] == r[{b}])'

        return s.replace(f'r[{self.ip_register}]', 'ip')


def parse(puzzle_input: str):
    """Parse input"""
    ip_str, program_str = puzzle_input.split('\n', 1)
    ip = int(ip_str.split()[1])

    program: list[Instruction] = []
    for line in program_str.split('\n'):
        i, a, b, c = line.split()
        program.append((i, int(a), int(b), int(c)))
    return ip, program


def part1(data):
    """Solve part 1"""
    ip, program = data
    device: Device = Device(ip)

    device.run(program)
    return device.registers[0]


def part2(data):
    """Solve part 2"""
    # ip, program = data
    # device: Device = Device(ip)
    # device.registers[0] = 1
    # device.run(program)
    # return device.registers[0]

    # for i, instruction in enumerate(program):
    #     print(f'{i}: {device.decompile(instruction)}')

    # From program reverse engineering
    r0: int = 0
    big_num: int = 10551331
    for i in range(1, big_num + 1):
        if big_num % i != 0:  # Added for speed up
            continue
        for j in range(1, big_num + 1):
            if i * j == big_num:
                r0 += i
    return r0


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None
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
