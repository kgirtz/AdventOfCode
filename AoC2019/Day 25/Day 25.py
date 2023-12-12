import pathlib
import sys
import os
from typing import Optional

sys.path.append('..')
from intcode import IntcodeComputer


class ItemDroid:
    def __init__(self, program: list[int]) -> None:
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program
        self.inventory: set[str] = set()

    def explore(self, cmds: Optional[list[str]] = None) -> str:
        self.computer.execute(self.program)
        print(self.computer.output_ASCII())

        if cmds is None:
            cmds = []
        else:
            cmds.reverse()

        past_sensor: bool = False
        while True:
            if cmds:
                cmd: str = cmds.pop()
            else:
                if not past_sensor:
                    self.determine_proper_weight()
                    past_sensor = True
                    return self.computer.output_ASCII()
                cmd: str = input('> ').strip().lower()

            match cmd.split()[0]:
                case 'north' | 'south' | 'east' | 'west' | 'inv':
                    self.computer.run_ASCII(f'{cmd}\n')
                case 'take' | 'drop':
                    cmd = ' '.join(cmd.split())
                    self.computer.run_ASCII(f'{cmd}\n')
                case _:
                    print(f'INVALID COMMAND: {cmd}')

    def determine_proper_weight(self) -> None:
        # Update inventory
        self.computer.run_ASCII('inv\n')
        items: str = self.computer.output_ASCII().split('\n\n')[0]
        self.inventory = {item.strip() for item in items.split('-')[1:]}

        for combo in combinations(self.inventory.copy()):
            if self.try_items(combo):
                return

    def try_items(self, items: set[str]) -> bool:
        for item in self.inventory - items:
            self.computer.run_ASCII(f'drop {item}\n')
        self.inventory &= items
        for item in items - self.inventory:
            self.computer.run_ASCII(f'take {item}\n')
        self.inventory |= items

        result: str = self.computer.run_ASCII(f'west\n')
        return not ('heavier' in result or 'lighter' in result)


def combinations(lst: set[str]) -> list[set[str]]:
    if len(lst) == 2:
        return [lst]

    combos: list[set[str]] = []
    for item in lst:
        for combo in combinations(lst - {item}):
            if combo not in combos:
                combos.append(combo)
            if combo | {item} not in combos:
                combos.append(combo | {item})

    return combos


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    droid: ItemDroid = ItemDroid(data)

    cmds: list[str] = ['east',
                       'take sand',
                       'west',
                       'south',
                       'take ornament',
                       'north',
                       'west',
                       'north',
                       'take wreath',
                       'north',
                       'north',
                       'take spool of cat6',
                       'south',
                       'south',
                       'east',
                       'take fixed point',
                       'west',
                       'south',
                       'south',
                       'south',
                       'take candy cane',
                       'north',
                       'east',
                       'east',
                       'east',
                       'take space law space brochure',
                       'south',
                       'take fuel cell',
                       'south']

    return droid.explore(cmds)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
