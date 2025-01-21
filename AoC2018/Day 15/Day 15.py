import pathlib
import sys
import os
import dataclasses
from collections.abc import Collection, Iterable

from space import Space
from xypair import XYpair, XYtuple, reading_order


@dataclasses.dataclass
class Unit:
    race: str
    position: XYpair
    attack: int = 3
    hp: int = 200

    def __lt__(self, other) -> bool:
        return reading_order(self.position) < reading_order(other.position)

    def take_damage(self, damage: int) -> None:
        self.hp -= damage

    def is_dead(self) -> bool:
        return self.hp <= 0


class Battle(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.walls: set[XYpair] = self.items['#']
        self.goblins: set[XYpair] = self.items['G']
        self.elves: set[XYpair] = self.items['E']
        self.units: list[Unit] = [Unit('GOBLIN', pt) for pt in self.items['G']] + \
                                 [Unit('ELF', pt) for pt in self.items['E']]
        self.rounds_completed: int = 0

    def combat_is_over(self) -> bool:
        return not self.goblins or not self.elves

    def move(self, unit: Unit, destination: XYpair) -> None:
        if unit.race == 'GOBLIN':
            self.goblins.remove(unit.position)
            self.goblins.add(destination)
        else:
            self.elves.remove(unit.position)
            self.elves.add(destination)
        unit.position = destination

    def first_steps_on_shortest_paths(self, start: XYtuple, finish: XYtuple) -> set[XYpair]:
        return {path[1] for path in self.min_paths(start, [finish])[finish]}  # noqa

    def round(self) -> None:
        for unit in sorted(self.units):
            if unit.is_dead():
                continue

            if self.combat_is_over():
                return

            # Identify targets
            targets: list[Unit] = [opp for opp in self.units if unit.race != opp.race]

            # Already in range?
            targets_in_range: list[Unit] = [t for t in targets if unit.position.adjacent(t.position)]
            if not targets_in_range:
                # Move

                # Identify open squares in range of each target
                in_range_of_targets: set[XYpair] = set()
                for target in targets:
                    in_range_of_targets.update(target.position.neighbors())
                in_range_of_targets -= self.walls | self.goblins | self.elves
                if not in_range_of_targets:
                    continue

                # Determine reachable points fewest steps away
                nearest: Collection[XYpair] = self.reachable_in_fewest_steps(unit.position, in_range_of_targets)[0]
                if len(nearest) == 0:
                    continue

                destination: XYpair = min(nearest, key=reading_order)
                next_steps: Iterable[XYpair] = self.first_steps_on_shortest_paths(unit.position, destination)
                next_step: XYpair = min(next_steps, key=reading_order)
                self.move(unit, next_step)

                targets_in_range = [t for t in targets if unit.position.adjacent(t.position)]

            if not targets_in_range:
                continue

            # Attack
            min_hp: int = min(t.hp for t in targets_in_range)
            weakest_target: Unit = min(t for t in targets_in_range if t.hp == min_hp)
            weakest_target.take_damage(unit.attack)
            if weakest_target.is_dead():
                self.units.remove(weakest_target)
                self.goblins.discard(weakest_target.position)
                self.elves.discard(weakest_target.position)

        self.rounds_completed += 1

    def outcome(self) -> int:
        return sum(unit.hp for unit in self.units) * self.rounds_completed


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    battle: Battle = Battle(data)
    while not battle.combat_is_over():
        battle.round()
    return battle.outcome()


def part2(data):
    """Solve part 2"""
    elf_count: int = len(Battle(data).elves)

    elf_attack_power: int = 4
    while True:
        battle: Battle = Battle(data)
        for u in battle.units:
            if u.race == 'ELF':
                u.attack = elf_attack_power

        while len(battle.elves) == elf_count and not battle.combat_is_over():
            battle.round()

        if len(battle.elves) == elf_count:
            return battle.outcome()

        elf_attack_power += 1


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 27730
    PART2_TEST_ANSWER = 4988

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
