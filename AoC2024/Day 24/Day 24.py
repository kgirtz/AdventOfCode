import pathlib
import sys
import os


class Gate:
    def __init__(self, definition: str) -> None:
        pieces: list[str] = definition.split()

        self.inputs: frozenset[str] = frozenset((pieces[0], pieces[2]))
        self.operation: str = pieces[1]
        self.output: str = pieces[4]

    def evaluate(self, input1: bool | None, input2: bool | None) -> bool | None:
        match self.operation:
            case 'AND':
                if input1 is False or input2 is False:
                    return False
                if input1 is None or input2 is None:
                    return None
                return True
            case 'OR':
                if input1 is True or input2 is True:
                    return True
                if input1 is None or input2 is None:
                    return None
                return False
            case 'XOR':
                if input1 is None or input2 is None:
                    return None
                return input1 ^ input2


def propagate(wires: dict[str, bool], gates: dict[str, Gate]) -> None:
    to_evaluate: set[str] = set(gates.keys())
    while to_evaluate:
        for wire in tuple(to_evaluate):
            input1, input2 = gates[wire].inputs
            result: bool | None = gates[wire].evaluate(wires.get(input1, None), wires.get(input2, None))
            if result is not None:
                wires[wire] = result
                to_evaluate.remove(wire)


def bus_value(bus: str, wires: dict[str, str]) -> int:
    bits: list[str] = sorted((wire for wire in wires if wire.startswith(bus)), reverse=True)
    return int(''.join(str(int(wires[bit])) for bit in bits), 2)


def swapped_wires(gates: dict[str, Gate], num_swaps: int) -> set[str]:
    """ Logical circuit structure:
        z00   =  x00  XOR y00                c00  =  x00  AND y00
        z[N]  = (x[N] XOR y[N]) XOR c[N-1]   c[N] = (x[N] AND y[N]) OR ((x[N] XOR y[N]) AND c[N-1])
        z[45] = c[44]
    """
    incorrect: set[str] = set()
    for output, gate in gates.items():
        internal_inputs: set[str] = gate.inputs & gates.keys()

        match gate.operation:
            case 'OR':
                # z values never come directly from OR gates (except the final carry bit)
                if output.startswith('z') and output != 'z45':
                    incorrect.add(output)

                # All inputs to OR gates must come from AND gates
                incorrect.update(i for i in gate.inputs if gates[i].operation != 'AND')

            case 'AND':
                # z values never come directly from AND gates
                if output.startswith('z'):
                    incorrect.add(output)

                # All non-xy inputs to AND gates cannot come from AND gates
                incorrect.update(i for i in internal_inputs if gates[i].operation == 'AND' and gates[i].inputs != {'x00', 'y00'})

            case 'XOR':
                # All XOR gates with non-xy inputs output z directly
                if internal_inputs and not output.startswith('z'):
                    incorrect.add(output)

                # All XOR gates with xy inputs cannot output z directly (except the LSB z00)
                elif not internal_inputs and output.startswith('z') and output != 'z00':
                    incorrect.add(output)

    if len(incorrect) != 2 * num_swaps:
        raise ValueError(f'needed {2 * num_swaps} incorrect wires ({num_swaps} swaps), found {len(incorrect)}')
    return incorrect


def parse(puzzle_input: str):
    """Parse input"""
    values_str, gate_str = puzzle_input.split('\n\n')

    wires: dict[str, bool] = {}
    for line in values_str.split('\n'):
        wire, value = line.split(': ')
        wires[wire] = value == '1'

    gates: dict[str, Gate] = {}
    for line in gate_str.split('\n'):
        output: str = line.split()[-1]
        gates[output] = Gate(line)

    return wires, gates


def part1(data):
    """Solve part 1"""
    wires, gates = data
    propagate(wires, gates)
    return bus_value('z', wires)


def part2(data):
    """Solve part 2"""
    _, gates = data
    return ','.join(sorted(swapped_wires(gates, 4)))


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 2024
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
