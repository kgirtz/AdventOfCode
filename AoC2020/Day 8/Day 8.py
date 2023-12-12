import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


class HandheldGameConsole:
    def __init__(self) -> None:
        self.accumulator: int = 0
        self.pc: int = 0

    @staticmethod
    def parse_instruction(instruction: str) -> tuple[str, int]:
        mnemonic, operand = instruction.split()
        return mnemonic, int(operand)

    def execute(self, instruction: str) -> None:
        mnemonic, operand = self.parse_instruction(instruction)

        if mnemonic == 'acc':
            self.accumulator += operand
            self.pc += 1
        elif mnemonic == 'jmp':
            self.pc += operand
        else:
            self.pc += 1

    def run(self, instructions: list[str], break_on_loop: bool = False, start: int = 0) -> None:
        executed: set[int] = set()
        self.pc = start
        self.accumulator = 0
        while self.pc < len(instructions):
            if break_on_loop and self.pc in executed:
                return
            executed.add(self.pc)
            self.execute(instructions[self.pc])

    def terminal_lines(self, instructions: list[str]) -> set[int]:
        line_nums: set[int] = set()
        line_count: int = 1
        while len(line_nums) != line_count:
            line_count: int = len(line_nums)
            for i in range(len(instructions) - 1, -1, -1):
                if i not in line_nums:
                    mnemonic, operand = self.parse_instruction(instructions[i])
                    if mnemonic != 'jmp' and (i == len(instructions) - 1 or i + 1 in line_nums):
                        line_nums.add(i)
                    elif mnemonic == 'jmp' and (i + operand in line_nums or i + operand == len(instructions)):
                        line_nums.add(i)
        return line_nums


def part1(data):
    """Solve part 1"""
    device: HandheldGameConsole = HandheldGameConsole()
    device.run(data, True)
    return device.accumulator


def part2(data):
    """Solve part 2"""
    device: HandheldGameConsole = HandheldGameConsole()
    terminal_line_nums: set[int] = device.terminal_lines(data)
    patch_idx: int = 0
    patch: str = ''
    i: int = 0
    while i < len(data):
        mnemonic, operand = device.parse_instruction(data[i])
        if mnemonic == 'jmp' and i + 1 in terminal_line_nums:
            patch_idx = i
            patch = f'nop {operand}'
            break
        elif mnemonic == 'nop' and i + operand in terminal_line_nums:
            patch_idx = i
            patch = f'jmp {operand}'
            break

        if mnemonic == 'jmp':
            i += operand
        else:
            i += 1

    if patch:
        data[patch_idx] = patch
        device.run(data)
        return device.accumulator


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
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
