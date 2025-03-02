import abc
import collections
import typing


class SpecialRegister:
    def __set_name__(self, _, name: str) -> None:
        self.name: str = name
        self.key: str = f'__{name}__'

    def __get__(self, computer, _=None) -> int:
        if computer is None:
            raise AttributeError(f'{self.name} has no class value')
        return computer.register[self.key]

    def __set__(self, computer, value: int) -> None:
        computer.register[self.key] = value


class AbstractComputer(abc.ABC):
    # Set a specific register as the program counter
    ip: SpecialRegister = SpecialRegister()

    # fetch/decode/execute return status codes
    SUCCESS: int = 0
    HALT: int = 1
    WAIT_FOR_INPUT: int = 2

    # step return status
    CONTINUE: bool = True
    BREAK: bool = False

    # Configure number of clock cycles per instruction
    DEFAULT_CYCLES_PER_INSTRUCTION: int = 1
    CYCLES_PER_INSTRUCTION: dict[str | int, int] = {}
    
    def __init__(self) -> None:
        self.register: dict[str | int, int] = collections.defaultdict(int)
        self._memory: dict[int, str | int] = {}
        self.instruction: collections.abc.Iterable[str | int] = ''
        self.opcode: str | int = ''
        self.operands: tuple[str | int, ...] = tuple()
        self._input_buffer: collections.deque[int] = collections.deque()
        self._output_buffer: collections.deque[int] = collections.deque()
        
        # Statistics
        self.clock_cycles: int = 0
        self.instruction_cycles: int = 0
        self.instruction_count: dict[str | int, int] = collections.defaultdict(int)
        self.inputs_processed: int = 0
        self.outputs_generated: int = 0
        self.addresses_executed: set[int] = set()
        
        # Initialize
        self.reset()
        self.clear_memory()
    
    def reset(self) -> None:
        """ When overwriting in subclasses call super().reset() before setting new attributes. """
        self.clear_registers()
        self.instruction = ''
        self.opcode = ''
        self.operands = tuple()
        self.clear_input_buffer()
        self.clear_output_buffer()

        self.clock_cycles = 0
        self.instruction_cycles = 0
        self.instruction_count = collections.defaultdict(int)
        self.addresses_executed = set()

    def clear_registers(self) -> None:
        self.register = collections.defaultdict(int)
    
    def read_memory(self, address: int) -> str | int:
        return self._memory[address]
    
    def write_memory(self, address: int, value: str | int) -> None:
        self._memory[address] = value
    
    def clear_memory(self) -> None:
        self._memory = {}
    
    def load_memory(self, memory_image: collections.abc.Iterable[str | int]) -> None:
        for address, data in enumerate(memory_image):
            self.write_memory(address, data)
    
    def allocated_memory(self) -> int:
        return len(self._memory)

    def input_available(self) -> bool:
        return self.input_buffer_length() > 0

    def clear_input_buffer(self) -> None:
        self._input_buffer = collections.deque()
        self.inputs_processed = 0

    def input_buffer_length(self) -> int:
        return len(self._input_buffer)

    def next_input(self) -> int:
        self.inputs_processed += 1
        return self._input_buffer.popleft()

    def add_to_input_buffer(self, inputs: collections.abc.Iterable[int]) -> None:
        self._input_buffer.extend(inputs)

    def output_available(self) -> bool:
        return self.output_buffer_length() > 0

    def clear_output_buffer(self) -> None:
        self._output_buffer = collections.deque()
        self.outputs_generated = 0

    def output_buffer_length(self) -> int:
        return len(self._output_buffer)

    def next_output(self) -> int:
        return self._output_buffer.popleft()

    def add_to_output_buffer(self, output_value: int) -> None:
        self._output_buffer.append(output_value)
        self.outputs_generated += 1

    def send_to(self, peer: typing.Self) -> None:
        if self.output_available():
            peer.add_to_input_buffer([self.next_output()])

    def receive_from(self, peer: typing.Self) -> None:
        peer.send_to(self)

    def run(self) -> None:
        while self.step() == self.CONTINUE:
            ...
    
    def step(self) -> bool:
        """ Execute a single instruction.
            return:
                True = ready to run next instruction
                False = error or halted (IP points outside program address space or waiting for input)
        """
        if self.fetch() == self.HALT:
            return self.BREAK

        if self.decode() == self.WAIT_FOR_INPUT:
            # Repeat current instruction
            self.ip = self.current_instruction_address()
            return self.BREAK

        # Add before execute in case a jump modifies IP
        self.addresses_executed.add(self.current_instruction_address())

        result: int = self.execute()

        # Update stats
        self.clock_cycles += self.current_instruction_clock_cycles()
        self.instruction_cycles += 1
        self.instruction_count[self.opcode] += 1

        return self.BREAK if result == self.HALT else self.CONTINUE

    def current_instruction_clock_cycles(self) -> int:
        """ Only valid after calling fetch() """
        return self.CYCLES_PER_INSTRUCTION.get(self.opcode, self.DEFAULT_CYCLES_PER_INSTRUCTION)

    @staticmethod
    def instruction_length() -> int:
        """ Overwrite to change fixed instruction width or implement variable-width instructions. """
        return 1

    def current_instruction_address(self) -> int:
        return self.ip - self.instruction_length()

    @staticmethod
    def immediate_value(operand: str | int, base: int = 10) -> int:
        return int(operand, base)

    def register_or_immediate_operand_value(self, operand: str | int, base: int = 10) -> int:
        try:
            return self.immediate_value(operand, base)
        except ValueError:
            return self.register[operand]

    def memory_operand(self, operand: str | int, base: int = 10) -> int:
        return self.read_memory(int(operand, base))
    
    def jump_absolute(self, address: int) -> None:
        self.ip = address
    
    def jump_relative(self, offset: int) -> None:
        """ Fetch already updated IP to next instruction so undo and add the offset. """
        self.ip = self.current_instruction_address() + offset
    
    def fetch(self) -> int | None:
        """ Get instruction pointed to by IP. """
        if not self.allocated_memory():
            raise RuntimeError('no program loaded')
        
        try:
            self.instruction = self.read_memory(self.ip)
        except LookupError:
            # IP is outside program address space
            return self.HALT

        self.ip += self.instruction_length()
        return self.SUCCESS
    
    def decode(self) -> int | None:
        """ Overwrite to interpret opcode and operands for each instruction as immediate, register, memory, etc.
            Default opcode behavior: get first symbol of space-separated string.
            Default operand behavior: convert all string operands into immediate base-10 integer values.
            If program waits for I/O, return HALT after checking opcode and buffer
        """
        self.instruction = typing.cast(str, self.instruction)
        self.opcode, *operands = self.instruction.split()
        self.operands = tuple(self.immediate_value(op) for op in operands)
        return self.SUCCESS

    @abc.abstractmethod
    def execute(self) -> int | None:
        """ Overwrite to define operation for each opcode. """


class Computer(AbstractComputer):
    def execute(self) -> None:
        if self.opcode == 'add':
            x, y = self.operands
            self.register['a'] = x + y
        if self.opcode == 'sub':
            x, y = self.operands
            self.register['a'] = x - y
        if self.opcode == 'mul':
            x, y = self.operands
            self.register['a'] = x * y
        if self.opcode == 'div':
            x, y = self.operands
            self.register['a'] = x // y
        if self.opcode == 'set':
            x, = self.operands
            self.register['b'] = x


prog = ['add 3 8', 'mul 2 7', 'set 100']
comp = Computer()
comp.load_memory(prog)
assert comp.register['a'] == 0 and comp.register['b'] == 0
comp.reset()
comp.run()
assert comp.register['a'] == 14 and comp.register['b'] == 100
