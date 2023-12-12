import pathlib
import sys
import os
import parse as scanf


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


class Computer:
    def __init__(self) -> None:
        self.memory: dict[[int, str], int] = {}
        self.mask: str = ''
        self.version: int = 1

    def memory_sum(self) -> int:
        if self.version == 1:
            return sum(self.memory.values())

        if self.version == 2:
            total: int = 0
            for address, value in self.memory.items():
                total += value * pow(2, address.count('X'))
            return total

    @staticmethod
    def overlap(a: str, b: str) -> bool:
        for i in range(len(a)):
            if a[i] != 'X' and b[i] != 'X' and a[i] != b[i]:
                return False
        return True

    def unaffected(self, old: str, new: str) -> set[str]:
        results: set[str] = {old}
        for i in range(len(old)):
            if old[i] == 'X' and new[i] != 'X':
                for address in results.copy():
                    results.remove(address)
                    results.add(address[:i] + '0' + address[i + 1:])
                    results.add(address[:i] + '1' + address[i + 1:])
        return {r for r in results if not self.overlap(r, new)}

    def mask_value(self, value: int) -> int:
        set_mask: int = int(self.mask.replace('X', '0'), 2)
        clear_mask: int = int(self.mask.replace('X', '1'), 2)
        return value & clear_mask | set_mask

    def mask_address(self, address: int) -> str:
        result: list[str] = list(f'{address:036b}')
        for i, bit in enumerate(self.mask):
            if bit in '1X':
                result[i] = bit
        return ''.join(result)

    def write_memory(self, address: int, value: int) -> None:
        if self.version == 1:
            self.memory[address] = self.mask_value(value)

        elif self.version == 2:
            destination: str = self.mask_address(address)
            allocated: set[str] = set(self.memory.keys())
            for addr in allocated:
                if self.overlap(addr, destination):
                    for remainder in self.unaffected(addr, destination):
                        self.memory[remainder] = self.memory[addr]
                    del self.memory[addr]
            self.memory[destination] = value

    def run(self, program: list[str]) -> None:
        for instruction in program:
            if instruction.startswith('mask'):
                self.mask = scanf.parse('mask = {}', instruction)[0]
            elif instruction.startswith('mem'):
                address, value = scanf.parse('mem[{:d}] = {:d}', instruction)
                self.write_memory(address, value)


def part1(data):
    """Solve part 1"""
    comp: Computer = Computer()
    comp.run(data)
    return comp.memory_sum()


def part2(data):
    """Solve part 2"""
    comp: Computer = Computer()
    comp.version = 2
    comp.run(data)
    return comp.memory_sum()


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
