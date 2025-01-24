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
    
    def decompile(self, program: Sequence[Instruction], *, hex_constants: bool = False) -> str:
        instructions: list[str] = []
        for address, instruction in enumerate(program):
            line: str = self.analyze(instruction, address)
            if hex_constants and 'goto' not in line and '(' not in line and 'ip' not in line:
                left, eq, *ops = line.split()
                line = f'{left} {eq}'
                for op in ops:
                    line += ' '
                    if len(op) > 1:
                        try:
                            op = hex(int(op))
                        except ValueError:
                            pass
                    line += op
                        
            instructions.append(f'{address}: ' + line)
        
        for i in range(len(instructions)):
            instruction: str = instructions[i]
            if 'goto' in instruction:
                dest = int(instruction.split('goto')[-1])
                if 0 <= dest < len(program):
                    target: str = instructions[dest]
                    if target[0] != '\n':
                        instructions[dest] = f'\n{target}'
                else:
                    instructions[i] = instructions[i].replace(f'goto {dest}', 'HALT')
                instructions[i] += '\n'
        
        return '\n'.join(instructions).replace('\n\n\n', '\n\n')

    def analyze(self, instruction: Instruction, address: int) -> str:
        opcode, a, b, c = instruction

        s: str = ''
        match opcode:
            case 'addr':
                s = f'r[{c}] = r[{a}] + r[{b}]'
            case 'addi':
                s = f'r[{c}] = r[{a}] + {b}'
            case 'mulr':
                s = f'r[{c}] = r[{a}] * r[{b}]'
            case 'muli':
                s = f'r[{c}] = r[{a}] * {b}'
            case 'banr':
                s = f'r[{c}] = r[{a}] & r[{b}]'
            case 'bani':
                s = f'r[{c}] = r[{a}] & {b}'
            case 'borr':
                s = f'r[{c}] = r[{a}] | r[{b}]'
            case 'bori':
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
        
        # Replace ip register with ip symbol
        s = s.replace(f'r[{self.ip_register}]', 'ip')
        
        # Get left and right hand sides of Instruction
        left, right = s.split(' = ')
        
        # Replace ip operands with current address
        right = right.replace('ip', str(address))
        
        # Evaluate constant operands in arithmetic instructions
        if '(' not in right and 'r' not in right:
            right = str(eval(right))
        
        # Alias ip assignments with goto statements
        if left == 'ip' and 'r' not in right:
            s = f'goto {int(right) + 1}'
        else:
            s = f'{left} = {right}'
        
        # Make operation in place if destination matches an operand
        if '(' not in right and len(right.split()) == 3:
            dst, eq, op1, sym, op2 = s.split()
            if dst == op1:
                s = f'{dst} {sym}= {op2}'
            elif dst == op2:
                s = f'{dst} {sym}= {op1}'

        return s


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
    
    # print(device.decompile(program, hex_constants=True))
    
    # From program reverse engineering
    r3 = 0x10000
    r4 = 0x9ce9f7
    
    while True:
        r4 = (r4 + (r3 & 0xff)) & 0xffffff
        r4 = (r4 * 0x1016b) & 0xffffff
        if r3 < 0x100:
            r0 = r4
            break
        r3 >>= 8
    
    device.registers[0] = r0
    device.run(program)
    
    return r0


def part2(data):
    """Solve part 2"""
    ip, program = data
    device: Device = Device(ip)
    
    # print(device.decompile(program, hex_constants=True))
    
    # From program reverse engineering
    seen = set()
    last_seen = -1
    r0 = -1
    r4 = 0
    while r0 < 0:
        r3 = r4 | 0x10000
        r4 = 0x9ce9f7
        
        while True:
            r4 = (r4 + (r3 & 0xff)) & 0xffffff
            r4 = (r4 * 0x1016b) & 0xffffff
            if r3 < 0x100:
                if r4 in seen:
                    r0 = last_seen
                last_seen = r4
                seen.add(r4)
                break
            r3 >>= 8
    
    device.registers[0] = r0
    # device.run(program)  # Takes a long time, but should HALT
    
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
