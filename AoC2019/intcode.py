from collections.abc import Iterable, Reversible

DEBUG = False


class IntcodeComputer:
    def __init__(self) -> None:
        self.pc: int = 0
        self.state: str = 'CREATED'
        self.input: list[int] = []
        self.output: list[int] = []
        self.memory: dict[int, int] = {}
        self.relative_base: int = 0

    def initialize(self, intcode: Iterable[int], noun: int | None = None, verb: int | None = None) -> None:
        self.pc = 0
        self.state = 'READY'
        self.input.clear()
        self.output.clear()
        self.memory = {i: byte for i, byte in enumerate(intcode)}
        self.relative_base = 0

        if noun is not None:
            self.memory[1] = noun
        if verb is not None:
            self.memory[2] = verb

    def src_operand(self, position: int) -> tuple[int, str]:
        value: int = self.memory[self.pc + position]
        mode: int = self.memory[self.pc] // 100
        for i in range(position - 1):
            mode //= 10
        mode %= 10

        match mode:
            case 0:
                op: int = self.memory.get(value, 0)
                return op, f'[{value}]=>{op}'
            case 1:
                return value, str(value)
            case 2:
                op = self.memory.get(value + self.relative_base, 0)
                return op, f'[{value} + {self.relative_base}]=>{op}'

    def dst_operand(self, position: int) -> tuple[int, str]:
        value: int = self.memory[self.pc + position]
        mode: int = self.memory[self.pc] // 100
        for i in range(position - 1):
            mode //= 10
        mode %= 10

        match mode:
            case 0:
                return value, f'{value}'
            case 2:
                return value + self.relative_base, f'{value} + {self.relative_base}'

    def execute_instruction(self) -> None:
        opcode: int = self.memory[self.pc] % 100
        prefix: str = f"{self.pc} ({self.memory[self.pc]}):"

        # Math and comparisons
        match opcode:
            case 1 | 2 | 7 | 8:
                src1, src1_str = self.src_operand(1)
                src2, src2_str = self.src_operand(2)
                dst, dst_str = self.dst_operand(3)

                match opcode:
                    case 1:  # add
                        if DEBUG:
                            print(f'{prefix} [{dst_str}] = {src1_str} + {src2_str}')
                        self.memory[dst] = src1 + src2
                    case 2:  # mult
                        if DEBUG:
                            print(f'{prefix} [{dst_str}] = {src1_str} * {src2_str}')
                        self.memory[dst] = src1 * src2
                    case 7:  # less than
                        if DEBUG:
                            print(f'{prefix} [{dst_str}] =  ({src1_str} < {src2_str})')
                        self.memory[dst] = 1 if src1 < src2 else 0
                    case 8:  # equals
                        if DEBUG:
                            print(f'{prefix} [{dst_str}] = ({src1_str} == {src2_str})')
                        self.memory[dst] = 1 if src1 == src2 else 0
                self.pc += 4

            # I/O
            case 3:  # input
                if not self.input:
                    self.state = 'PAUSED'
                    return

                dst, dst_str = self.dst_operand(1)
                if DEBUG:
                    print(f'{prefix} [{dst_str}] << {self.input[-1]}')
                self.memory[dst] = self.input.pop()
                self.pc += 2

            case 4:  # output
                src, src_str = self.src_operand(1)
                if DEBUG:
                    print(f'{prefix} {src} >> output')
                self.output.append(src)
                self.pc += 2

            # Jumps
            case 5 | 6:
                condition, cond_str = self.src_operand(1)
                target, target_str = self.src_operand(2)

                if opcode == 5:  # jump if not zero
                    if DEBUG:
                        print(f'{prefix} if ({cond_str}) goto {target_str}')
                    if condition != 0:
                        self.pc = target
                    else:
                        self.pc += 3
                elif opcode == 6:  # jump if zero
                    if DEBUG:
                        print(f'{prefix} if !({cond_str}) goto {target_str}')
                    if condition == 0:
                        self.pc = target
                    else:
                        self.pc += 3

            # Addressing
            case 9:  # Modify relative base
                src, src_str = self.src_operand(1)

                if DEBUG:
                    print(f'{prefix} REL_BASE += {src_str}')
                self.relative_base += src
                self.pc += 2

            # Execution state
            case 99:  # halt
                if DEBUG:
                    print(f'{prefix} HALT')
                self.state = 'HALTED'

    def run(self, inputs: Reversible[int] | None = None) -> list[int]:
        if inputs is None:
            self.input = []
        else:
            self.input = list(reversed(inputs))

        self.output = []

        if self.state == 'HALTED':
            return []

        self.state = 'RUNNING'
        while self.state == 'RUNNING':
            self.execute_instruction()
        return self.output

    def run_ASCII(self, str_input: str = '') -> str:
        self.run([ord(ch) for ch in str_input])
        return self.output_ASCII()

    def execute(self, intcode: Iterable[int], inputs: Iterable[int] | None = None,
                noun: int | None = None, verb: int | None = None) -> list[int]:

        self.initialize(intcode, noun, verb)
        return self.run(inputs)

    def output_ASCII(self) -> str:
        output_str: str = ''
        for n in self.output:
            try:
                output_str += chr(n)
            except ValueError:
                output_str += '{{UNPRINTABLE}}'
        return output_str
