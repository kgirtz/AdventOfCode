import pathlib
import sys
import os


class ALU:
    def __init__(self) -> None:
        self.var: dict[str, int] = {reg: 0 for reg in 'wxyz'}

    def __str__(self) -> str:
        return str(self.var)

    def run(self, program: list[str], input_str: str = '') -> None:
        for instruction in program:
            input_str = self.execute(instruction, input_str)
        return

    def execute(self, instruction: str, input_str: str = '') -> str:
        if instruction.startswith('inp'):
            dst: str = instruction[-1]
            self.var[dst] = int(input_str[0])
            return input_str[1:]

        mnemonic, dst, op_str = instruction.split()
        if op_str[-1].isdigit():
            op = int(op_str)
        else:
            op = self.var[op_str]

        if mnemonic == 'add':
            self.var[dst] += op
        elif mnemonic == 'mul':
            self.var[dst] *= op
        elif mnemonic == 'div':
            self.var[dst] //= op
        elif mnemonic == 'mod':
            self.var[dst] %= op
        elif mnemonic == 'eql':
            self.var[dst] = int(self.var[dst] == op)

        return input_str


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    monad: list[str] = data
    unit: ALU = ALU()
    for d1 in range(8, 0, -1):  # 1:8
        for d2 in range(9, 6, -1):  # 7:9
            for d3 in range(9, 0, -1):  # 1:9
                for d4 in range(5, 0, -1):  # 1:5
                    for d5 in range(9, 4, -1):  # 5:9
                        for d6 in range(7, 0, -1):  # 1:7
                            for d7 in range(9, 2, -1):  # 3:9
                                for d8 in range(4, 0, -1):  # 1:4
                                    for d9 in range(9, 8, -1):  # 9
                                        for d10 in range(1, 0, -1):  # 1
                                            for d11 in range(9, 5, -1):  # 6:9
                                                for d12 in range(9, 0, -1):  # 1:9
                                                    for d13 in range(3, 0, -1):  # 1:3
                                                        for d14 in range(9, 1, -1):  # 2:9
                                                            model_num: str = ''.join(str(d) for d in [d1, d2, d3, d4,
                                                                                                     d5, d6, d7, d8,
                                                                                                     d9, d10, d11, d12,
                                                                                                     d13, d14])
                                                            unit.run(monad, model_num)
                                                            if unit.var['z'] == 0:
                                                                return int(model_num)


def part2(data):
    """Solve part 2"""
    monad: list[str] = data
    unit: ALU = ALU()
    for d1 in range(1, 9):  # 1:8
        for d2 in range(7, 10):  # 7:9
            for d3 in range(1, 10):  # 1:9
                for d4 in range(1, 6):  # 1:5
                    for d5 in range(5, 10):  # 5:9
                        for d6 in range(1, 8):  # 1:7
                            for d7 in range(3, 10):  # 3:9
                                for d8 in range(1, 5):  # 1:4
                                    for d9 in range(9, 10):  # 9
                                        for d10 in range(1, 2):  # 1
                                            for d11 in range(6, 10):  # 6:9
                                                for d12 in range(1, 10):  # 1:9
                                                    for d13 in range(1, 4):  # 1:3
                                                        for d14 in range(2, 10):  # 2:9
                                                            model_num: str = ''.join(str(d) for d in [d1, d2, d3, d4,
                                                                                                      d5, d6, d7, d8,
                                                                                                      d9, d10, d11, d12,
                                                                                                      d13, d14])
                                                            unit.run(monad, model_num)
                                                            if unit.var['z'] == 0:
                                                                return int(model_num)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):  # 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
