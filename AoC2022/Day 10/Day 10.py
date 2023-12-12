import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split('\n')


def opcode(instruction: str) -> str:
    return instruction.split()[0]


def operand(instruction: str) -> str:
    match opcode(instruction):
        case 'noop':
            return ''
        case 'addx':
            return instruction.split()[1]


def execute_instruction(instruction: str, x: int) -> int:
    match opcode(instruction):
        case 'noop':
            return x
        case 'addx':
            return x + int(operand(instruction))


def expanded_program(program: list[str]) -> list[str]:
    # Replace addx(2-cyc) with noop/addx(1-cyc)
    for instruction in program:
        match opcode(instruction):
            case 'noop':
                yield 'noop'
            case 'addx':
                yield 'noop'
                yield instruction


def execute_program(program: list[str], max_cycles: int = 0) -> int:
    x: int = 1
    cycle_count: int = 0

    for instruction in expanded_program(program):
        x = execute_instruction(instruction, x)
        cycle_count += 1
        if cycle_count == max_cycles:
            break

    return x


def render_crt(program: list[str]) -> str:
    pixel_width: int = 40
    pixel_height: int = 6
    pixel_total: int = pixel_height * pixel_width

    crt: list[str] = ['' for _ in range(pixel_total)]

    x: int = 1
    cycle_count: int = 0

    for instruction in expanded_program(program):
        pixel_pos: int = cycle_count % pixel_width
        if abs(pixel_pos - x) <= 1:
            crt[cycle_count] = '#'
        else:
            crt[cycle_count] = '.'

        if (pixel_pos + 1) % pixel_width == 0:
            crt[cycle_count] += '\n'

        x = execute_instruction(instruction, x)
        cycle_count += 1
        if cycle_count == pixel_total:
            break

    return ''.join(crt)


def part1(data):
    """Solve part 1"""
    interesting_cycles: list[int] = list(range(20, 220 + 1, 40))

    signal_strengths: list[int] = [execute_program(data, c - 1) * c for c in interesting_cycles]

    return sum(signal_strengths)


def part2(data):
    """Solve part 2"""

    return render_crt(data)


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
