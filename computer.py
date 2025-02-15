import abc
import collections
import typing

SUCCESS_CODE: int = 0
HALT_CODE: int = 1


def register_key(key: str | int) -> str | int:
    """ Convert numeric strings into integers. """
    try:
        return int(key)
    except ValueError:
        return key


class AbstractComputer(abc.ABC):
    # Set a specific register as the program counter
    IP_REGISTER: str | int = '_IP'
    
    def __init__(self) -> None:
        self._registers: dict[str | int, int] = collections.defaultdict(int)
        self._memory: dict[int, str | int] = {}
        self.instruction: collections.abc.Iterable[str | int] = ''
        self.opcode: str | int = ''
        self.operands: collections.abc.Iterable[str | int] = tuple()
        self._input_buffer: collections.deque[int] = collections.deque()
        self._output_buffer: collections.deque[int] = collections.deque()
        
        # Statistics
        self.instructions_executed: int = 0
        self.instruction_count: dict[str | int, int] = collections.defaultdict(int)
        
        # Initialize
        self.reset()
        self.clear_memory()
    
    @property
    def ip(self) -> int:
        """ Instruction Pointer """
        return self.register(self.IP_REGISTER)
    
    @ip.setter
    def ip(self, address: int) -> None:
        self.write_register(self.IP_REGISTER, address)
    
    def reset(self) -> None:
        """ When overwriting in subclasses call super().reset() before setting new attributes. """
        self.clear_registers()
        self.instruction = ''
        self.opcode = ''
        self.operands = tuple()
        self.clear_input_buffer()
        self.clear_output_buffer()
        
        self.instructions_executed = 0
        self.instruction_count = collections.defaultdict(int)
    
    def register(self, register: str | int) -> int:
        return self._registers[register_key(register)]
    
    def write_register(self, register: str | int, value: int) -> None:
        self._registers[register_key(register)] = value

    def clear_registers(self) -> None:
        self._registers = collections.defaultdict(int)
    
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
        return bool(self._input_buffer)

    def clear_input_buffer(self) -> None:
        self._input_buffer = collections.deque()

    def next_input(self) -> int:
        return self._input_buffer.popleft()

    def add_to_input_buffer(self, inputs: collections.abc.Iterable[int]) -> None:
        self._input_buffer.extend(inputs)

    def output_available(self) -> bool:
        return bool(self._output_buffer)

    def clear_output_buffer(self) -> None:
        self._output_buffer = collections.deque()

    def next_output(self) -> int:
        return self._output_buffer.popleft()

    def add_to_output_buffer(self, outputs: collections.abc.Iterable[int]) -> None:
        self._output_buffer.extend(outputs)

    def run(self) -> None:
        while self.step():
            pass
    
    def step(self) -> bool:
        """ Execute a single instruction.
            return:
                True = ready to run next instruction
                False = error or halted (IP points outside program address space or waiting for input)
        """
        if self.fetch() != SUCCESS_CODE:
            return False

        if self.decode() != SUCCESS_CODE:
            return False

        self.execute()
        
        # Count each instruction
        self.instructions_executed += 1
        self.instruction_count[self.opcode] += 1
        
        return True

    @staticmethod
    def instruction_length() -> int:
        """ Overwrite to change fixed instruction width or implement variable-width instructions. """
        return 1

    @staticmethod
    def immediate_operand(operand: str | int, base: int = 10) -> int:
        return int(operand, base)
    
    def register_operand(self, operand: str | int) -> int:
        return self.register(operand)

    def memory_operand(self, operand: str | int, base: int = 10) -> int:
        return self.read_memory(int(operand, base))
    
    def jump_absolute(self, address: int) -> None:
        self.ip = address
    
    def jump_relative(self, offset: int) -> None:
        """ Fetch already updated IP to next instruction so undo and add the offset. """
        self.ip += offset - self.instruction_length()
    
    def fetch(self) -> int:
        """ Get instruction pointed to by IP. """
        if not self.allocated_memory():
            raise RuntimeError('no program loaded')
        
        try:
            self.instruction = self.read_memory(self.ip)
        except LookupError:
            # IP is outside program address space
            return HALT_CODE

        self.ip += self.instruction_length()
        return SUCCESS_CODE
    
    def decode(self) -> int:
        """ Overwrite to interpret opcode and operands for each instruction as immediate, register, memory, etc.
            Default opcode behavior: get first symbol of space-separated string.
            Default operand behavior: convert all string operands into immediate base-10 integer values.
            If program waits for I/O, return HALT_CODE after checking opcode and buffer
        """
        self.instruction = typing.cast(str, self.instruction)
        self.opcode, *operands = self.instruction.split()
        self.operands = tuple(self.immediate_operand(op) for op in operands)
        return SUCCESS_CODE

    @abc.abstractmethod
    def execute(self) -> None:
        """ Overwrite to define operation for each opcode. """


class Computer(AbstractComputer):
    def execute(self) -> None:
        if self.opcode == 'add':
            x, y = self.operands
            self.write_register('a', x + y)
        if self.opcode == 'sub':
            x, y = self.operands
            self.write_register('a', x - y)
        if self.opcode == 'mul':
            x, y = self.operands
            self.write_register('a', x * y)
        if self.opcode == 'div':
            x, y = self.operands
            self.write_register('a', x // y)
        if self.opcode == 'set':
            x, = self.operands
            self.write_register('b', x)


prog = ['add 3 8', 'mul 2 7', 'set 100']
comp = Computer()
comp.load_memory(prog)
assert comp.register('a') == 0 and comp.register('b') == 0
comp.reset()
comp.run()
assert comp.register('a') == 14 and comp.register('b') == 100
