import pathlib
import sys
import os
from typing import Sequence


class Gate:
    def __init__(self, definition: str) -> None:
        pieces: list[str] = definition.split()

        self.inputs: list[str] = [pieces[0], pieces[2]]
        self.operation: str = pieces[1]
        self.output: str = pieces[4]

        self.inputs.sort()

        self.annotated_inputs: list[str] = []
        self.annotated_output: str = ''

    def __hash__(self) -> int:
        return hash(tuple(self.inputs) + (self.operation, self.output))

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
    bits: Sequence[str] = sorted((wire for wire in wires if wire.startswith(bus)), reverse=True)
    return int(''.join(str(int(wires[bit])) for bit in bits), 2)


def swapped_wires(wires: dict[str, bool], gates: dict[str, Gate], num_swaps: int) -> set[str]:
    incorrect: set[str] = set()
    for output, gate in gates.items():
        match gate.operation:
            case 'OR':
                if output.startswith('z') and output != 'z45':
                    incorrect.add(output)
                for inp in gate.inputs:
                    if gates[inp].operation != 'AND':
                        incorrect.add(inp)
            case 'AND':
                if output.startswith('z'):
                    incorrect.add(output)
                if set(gate.inputs) & set(gates.keys()):
                    for inp in gate.inputs:
                        if gates[inp].operation == 'AND':
                            if gates[inp].inputs != ['x00', 'y00']:
                                incorrect.add(inp)
            case 'XOR':
                # Inputs come from other gates
                if set(gate.inputs) & set(gates.keys()):
                    if not output.startswith('z'):
                        incorrect.add(output)
                # Inputs come from input values
                elif output.startswith('z') and output != 'z00':
                    incorrect.add(output)

    assert len(incorrect) == 2 * num_swaps
    return incorrect


def causal_network(output: str, gates: dict[str, Gate]) -> set[Gate]:
    network: set[Gate] = {gates[output]}
    inputs: set[str] = set()
    cur_wires: set[str] = set(gates[output].inputs)
    while cur_wires:
        wire = cur_wires.pop()
        if wire[0] in 'xyz':
            inputs.add(wire)
        elif wire in gates:
            network.add(gates[wire])
            cur_wires.update(gates[wire].inputs)

    # if int(output.lstrip('z')) != max(int(i.lstrip('xy')) for i in inputs):
    print(f'{output} is affected by {", ".join(sorted(inputs))}')
    return network


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
    wires, gates = data
    return ','.join(sorted(swapped_wires(wires, gates, 4)))


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
