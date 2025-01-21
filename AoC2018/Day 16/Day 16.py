import pathlib
import sys
import os
import re
import collections
from collections.abc import Sequence


class Device:
    opcode_list: tuple[str, ...] = ('eqri',  # 0
                                    'bani',  # 1
                                    'seti',  # 2
                                    'bori',  # 3
                                    'eqir',  # 4
                                    'banr',  # 5
                                    'borr',  # 6
                                    'muli',  # 7
                                    'setr',  # 8
                                    'addr',  # 9
                                    'eqrr',  # 10
                                    'addi',  # 11
                                    'gtir',  # 12
                                    'gtrr',  # 13
                                    'gtri',  # 14
                                    'mulr')  # 15

    def __init__(self, opcodes: Sequence[str] = tuple()) -> None:
        self.registers: list[int] = [0, 0, 0, 0]
        self.opcode_table: tuple[str, ...] = self.opcode_list
        if opcodes:
            assert sorted(opcodes) == sorted(self.opcode_list)
            self.opcode_table = tuple(opcodes)

    def set_registers(self, values: Sequence[int]) -> None:
        assert len(values) == 4
        self.registers = list(values)

    def execute(self, instruction: Sequence[int]) -> None:
        opcode, a, b, c = instruction

        match self.opcode_table[opcode]:
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


def parse(puzzle_input: str):
    """Parse input"""
    samples_str, program_str = puzzle_input.split('\n\n\n\n')

    samples: list[tuple[list[int], ...]] = []
    for sample in samples_str.split('\n\n'):
        nums: list[int] = [int(n) for n in re.findall(r'\d+', sample)]
        samples.append((nums[:4], nums[4:8], nums[8:]))

    program: list[list[int]] = [[int(n) for n in line.split()] for line in program_str.split('\n')]
    return samples, program


def part1(data):
    """Solve part 1"""  # 527 is too high
    samples, _ = data

    more_than_three_opcodes: int = 0
    opcode_options: dict[int, set[str]] = collections.defaultdict(set)
    for before, instruction, after in samples:
        opcode_num: int = instruction[0]

        potential_opcodes: set[str] = set()
        possible_mapping: list[str] = list(Device.opcode_list)
        for _ in range(len(possible_mapping)):
            device: Device = Device(possible_mapping)
            device.set_registers(before)
            device.execute(instruction)
            if device.registers == after:
                potential_opcodes.add(possible_mapping[opcode_num])
            possible_mapping = possible_mapping[1:] + [possible_mapping[0]]

        if len(potential_opcodes) >= 3:
            more_than_three_opcodes += 1

        if opcode_num not in opcode_options:
            opcode_options[opcode_num] = potential_opcodes
        else:
            opcode_options[opcode_num] &= potential_opcodes

    # Determine full opcode mapping
    while any(len(v) > 1 for v in opcode_options.values()):
        for v in opcode_options.values():
            if len(v) == 1:
                op: str = tuple(v)[0]
                for v in opcode_options.values():
                    if len(v) > 1:
                        v.discard(op)

    return more_than_three_opcodes


def part2(data):
    """Solve part 2"""
    _, program = data
    device: Device = Device()
    for instruction in program:
        device.execute(instruction)
    return device.registers[0]


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
