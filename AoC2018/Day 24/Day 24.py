import pathlib
import sys
import os
import re
import itertools
from collections.abc import Iterable
from typing import Self


class ArmyGroup:
    def __init__(self, description: str) -> None:
        units, hp, attack, initiative = re.findall(r'\d+', description)
        self.units: int = int(units)
        self.hp: int = int(hp)
        self.attack: int = int(attack)
        self.initiative: int = int(initiative)

        self.damage_type: str = re.search(r'\w+(?= damage)', description).group(0)

        self.weakness: frozenset[str] = frozenset()
        if 'weak' in description:
            self.weakness = frozenset(re.search(r'(?<=weak to )\w+[, \w+]*', description).group(0).split(', '))

        self.immunity: frozenset[str] = frozenset()
        if 'immune' in description:
            self.immunity = frozenset(re.search(r'(?<=immune to )\w+[, \w+]*', description).group(0).split(', '))

        self.target: ArmyGroup | None = None
        self.is_targeted: bool = False

        self.starting_units: int = self.units
        self.starting_attack: int = self.attack

    def __lt__(self, other: Self) -> bool:
        return (self.effective_power(), self.initiative) < (other.effective_power(), other.initiative)

    def reset(self) -> None:
        self.units = self.starting_units
        self.attack = self.starting_attack
        self.target = None
        self.is_targeted = False

    def is_immune_to(self, damage_type: str) -> bool:
        return damage_type in self.immunity

    def is_weak_to(self, damage_type: str) -> bool:
        return damage_type in self.weakness

    def effective_power(self) -> int:
        return self.units * self.attack

    def select_target(self, enemies: Iterable[Self]) -> None:
        enemies = [e for e in enemies if not e.is_targeted and not e.is_immune_to(self.damage_type)]
        if not enemies:
            self.target = None
            return

        weak: list[ArmyGroup] = [e for e in enemies if e.is_weak_to(self.damage_type)]
        if weak:
            enemies = weak

        self.target = max(enemies)
        self.target.is_targeted = True

    def attack_target(self) -> None:
        if self.target is None:
            return

        damage: int = self.effective_power()
        if self.target.is_immune_to(self.damage_type):
            damage = 0
        elif self.target.is_weak_to(self.damage_type):
            damage *= 2

        units_killed: int = damage // self.target.hp
        self.target.units = max(self.target.units - units_killed, 0)

        self.target.is_targeted = False
        self.target = None


def fight(immune_system_army: Iterable[ArmyGroup], infection_army: Iterable[ArmyGroup]) -> bool:
    # Target selection phase
    for group in sorted(immune_system_army, reverse=True):
        group.select_target(infection_army)
    for group in sorted(infection_army, reverse=True):
        group.select_target(immune_system_army)

    immune_units: int = sum(group.units for group in immune_system_army)
    infection_units: int = sum(group.units for group in infection_army)

    # Attack phase
    for group in sorted(itertools.chain(immune_system_army, infection_army), key=lambda g: -g.initiative):
        group.attack_target()

    # Check for stalemate
    return immune_units == sum(group.units for group in immune_system_army) and \
        infection_units == sum(group.units for group in infection_army)


def combat(immune_system_army: Iterable[ArmyGroup], infection_army: Iterable[ArmyGroup]) -> (list[ArmyGroup], list[ArmyGroup]):
    while immune_system_army and infection_army:
        # Check for stalemate
        if fight(immune_system_army, infection_army):
            break
        immune_system_army = [group for group in immune_system_army if group.units]
        infection_army = [group for group in infection_army if group.units]
    return immune_system_army, infection_army


def parse(puzzle_input: str):
    """Parse input"""
    immune_str, infection_str = puzzle_input.split('\n\n')
    immune_system_army: list[ArmyGroup] = [ArmyGroup(line) for line in immune_str.split('\n')[1:]]
    infection_army: list[ArmyGroup] = [ArmyGroup(line) for line in infection_str.split('\n')[1:]]
    return immune_system_army, infection_army


def part1(data):
    """Solve part 1"""
    immune_system_army, infection_army = data
    immune_system_army, infection_army = combat(immune_system_army, infection_army)
    return sum(group.units for group in immune_system_army + infection_army)


def part2(data):
    """Solve part 2"""
    immune_system_army, infection_army = data
    boost: int = 1
    while True:
        for group in itertools.chain(immune_system_army, infection_army):
            group.reset()
        for group in immune_system_army:
            group.attack += boost

        remaining_immune_system, remaining_infection_system = combat(immune_system_army, infection_army)
        if remaining_immune_system and not remaining_infection_system:
            return sum(group.units for group in remaining_immune_system)

        boost += 1


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 5216
    PART2_TEST_ANSWER = 51

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
