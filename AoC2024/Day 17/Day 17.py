import pathlib
import sys
import os
from typing import Sequence


def parse(puzzle_input: str):
    """Parse input"""
    registers_str, program_str = puzzle_input.split('\n\n')
    registers: list[int] = [int(line.split()[-1]) for line in registers_str.split('\n')]
    program: list[int] = [int(n) for n in program_str.split()[-1].split(',')]
    return registers, program


class Computer:
    def __init__(self) -> None:
        self.A: int = 0
        self.B: int = 0
        self.C: int = 0
        self.IP: int = 0
        self.output: list[int] = []

    def set_registers(self, *, a: int | None = None, b: int | None = None, c: int | None = None) -> None:
        if a is not None:
            self.A = int(a)
        if b is not None:
            self.B = int(b)
        if c is not None:
            self.C = int(c)

    def run(self, program: Sequence[int]) -> str:
        self.IP = 0
        self.output = []
        while self.IP < len(program):
            opcode, operand = program[self.IP:self.IP + 2]
            self.execute(opcode, operand)
            self.IP += 2
        return ','.join(str(n) for n in self.output)

    def combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise ValueError('reserved combo operand')

    def execute(self, opcode: int, operand: int) -> (int | None):
        match opcode:
            case 0:
                self.A = self.A >> self.combo_operand(operand)
            case 1:
                self.B ^= operand
            case 2:
                self.B = self.combo_operand(operand) & 0x7
            case 3:
                if self.A:
                    self.IP = operand - 2
            case 4:
                self.B ^= self.C
            case 5:
                value: int = self.combo_operand(operand) & 0x7
                self.output.append(value)
                return value
            case 6:
                self.B = self.A >> self.combo_operand(operand)
            case 7:
                self.C = self.A >> self.combo_operand(operand)


def part1(data):
    """Solve part 1"""
    (a, b, c), program = data
    computer: Computer = Computer()
    computer.set_registers(a=a, b=b, c=c)
    return computer.run(program)


def part2(data):
    """Solve part 2"""
    (a, b, c), program = data
    computer: Computer = Computer()

    program_str: str = ','.join(str(n) for n in program)
    split_program_str: list[str] = program_str.split(',')

    possible_a_values: set[int] = {0}
    correct: set[int] = set()
    for p in range(len(program)):
        print(p)
        new_possible: set[int] = set()
        for a in range(1, pow(2, 10)):
            a <<= p * 3
            for possible in sorted(possible_a_values):
                computer.set_registers(a=a + possible, b=b, c=c)
                result: str = computer.run(program)
                if len(result) <= len(program_str) and split_program_str[:p + 1] == result.split(',')[:p + 1]:
                    new_possible.add(a + possible)
                    if result == program_str:
                        correct.add(a + possible)
        if correct:
            return min(correct)
        possible_a_values = new_possible


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = '4,6,3,5,6,3,5,2,1,0'
    PART2_TEST_ANSWER = 117440

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
