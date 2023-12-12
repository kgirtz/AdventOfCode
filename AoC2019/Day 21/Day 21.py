import pathlib
import sys
import os

sys.path.append('..')
from intcode import IntcodeComputer


class SpringDroid:
    def __init__(self, program: list[int]) -> None:
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program

    @staticmethod
    def springscript_walk() -> str:
        script: list[str] = ['NOT A J',
                             'NOT B T',
                             'OR T J',
                             'NOT C T',
                             'OR T J',
                             'AND D J']
        return '\n'.join(script) + '\n'

    @staticmethod
    def springscript_run() -> str:
        script: list[str] = ['NOT A J',
                             'NOT B T',
                             'OR T J',
                             'NOT C T',
                             'OR T J',
                             'AND D J',
                             'NOT D T',
                             'OR E T',
                             'OR H T',
                             'AND T J']
        return '\n'.join(script) + '\n'

    def navigate_hull(self, mode: str = 'WALK') -> int:
        self.computer.execute(self.program)

        match mode:
            case 'WALK':
                springscript: str = SpringDroid.springscript_walk()
            case 'RUN':
                springscript: str = SpringDroid.springscript_run()
            case _:
                print(f'INVALID MODE: {mode}')
                return 0

        output: str = self.computer.run_ASCII(springscript + mode + '\n')
        if '{{UNPRINTABLE}}' in output:
            return self.computer.output[-1]
        else:
            print(self.computer.output_ASCII())
            return 0


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    droid: SpringDroid = SpringDroid(data)
    return droid.navigate_hull()


def part2(data):
    """Solve part 2"""
    droid: SpringDroid = SpringDroid(data)
    return droid.navigate_hull('RUN')


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
