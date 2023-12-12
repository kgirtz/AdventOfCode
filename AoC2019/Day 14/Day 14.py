import pathlib
import sys
import os
import math
from typing import Iterable, Sequence


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


class Nanofactory:
    UNASSIGNED: int = 1
    LOWEST: int = 2

    def __init__(self, reactions: Iterable[str]) -> None:
        self.ore_mem: dict[str, int] = {}
        self.excess_mem: dict[str, dict[str, int]] = {}
        self.num_produced: dict[str, int] = {'ORE': 0}
        self.recipe: dict[str, dict[str, int]] = {'ORE': {}}
        self.priority: dict[str, int] = {}

        for reaction in reactions:
            reactants_str, product_str = reaction.split('=>')

            reactants: dict[str, int] = {}
            for r in reactants_str.split(','):
                amount, reactant = r.split()
                reactants[reactant] = int(amount)

            amount, product = product_str.split()
            self.num_produced[product] = int(amount)

            self.recipe[product] = reactants

        self.priority = {chemical: self.UNASSIGNED for chemical in self.recipe}
        while self.UNASSIGNED in self.priority.values():
            for chemical, p in self.priority.items():
                if p != self.UNASSIGNED:
                    continue

                if chemical == 'ORE':
                    self.priority[chemical] = self.LOWEST
                elif self.recipe[chemical].keys() == {'ORE'}:
                    self.priority[chemical] = self.UNASSIGNED - 1
                else:
                    sub_priorities: list[int] = [self.priority[r] for r in self.recipe[chemical] if r != 'ORE']
                    if self.UNASSIGNED not in sub_priorities:
                        self.priority[chemical] = min(sub_priorities) - 1

    def get_priority(self, chemical: str) -> int:
        return self.priority[chemical]

    def num_reactions_needed(self, reactant: str, amount: int) -> int:
        return math.ceil(amount / self.num_produced[reactant])

    """def ore_required(self, chemical: str) -> tuple[int, dict[str, int]]:
        # Check for memoized result
        if chemical in self.ore_mem:
            return self.ore_mem[chemical], self.excess_mem[chemical]

        reactants: dict[str, int] = {r: amt for r, amt in self.recipe[chemical].items() if r != 'ORE'}

        # Get ore & reaction count for each reactant while aggregating excess
        ore: dict[str, int] = {}
        reaction_count: dict[str, int] = {}
        excess: dict[str, int] = {}
        for r, amt in reactants.items():
            ore_req, excess_produced = self.ore_required(r)
            ore[r] = ore_req
            reaction_count[r] = self.num_reactions_needed(r, amt)
            excess = dict_add(excess, dict_mult(excess_produced, reaction_count[r]))

        # Calculate total ore required & total reactants produced
        total_ore: int = self.recipe[chemical].get('ORE', 0)
        total_produced: dict[str, int] = {}
        for r in reactants:
            ore_required = ore[r]
            count = reaction_count[r]

            total_ore += count * ore_required
            total_produced[r] = count * self.num_produced[r]
        total_produced = dict_add(total_produced, excess)

        # Use up excess if possible
        for r in reactants.keys() & excess.keys():
            while reaction_count[r] > 0 and total_produced[r] - reactants[r] >= self.num_produced[r]:
                reaction_count[r] -= 1
                total_produced[r] -= self.num_produced[r]
                total_ore -= ore[r]
        total_excess: dict[str, int] = dict_sub(total_produced, reactants)

        # Memoize result
        self.ore_mem[chemical] = total_ore
        self.excess_mem[chemical] = total_excess
        return total_ore, total_excess"""

    def min_process(self, product: str) -> list[tuple[str, int]]:
        cur_chemicals: dict[str, int] = {chemical: 0 for chemical in self.recipe}

        process: list[tuple[str, int]] = []

        cur_chemicals[product] = self.num_produced[product]
        to_reduce: set[str] = {product}
        while to_reduce:
            cur_product: str = min(to_reduce, key=self.get_priority)
            to_reduce.remove(cur_product)
            cur_recipe: dict[str, int] = self.recipe[cur_product]
            num_to_reduce: int = cur_chemicals[cur_product]
            cur_chemicals[cur_product] = 0
            reaction_count: int = self.num_reactions_needed(cur_product, num_to_reduce)
            process.append((cur_product, num_to_reduce))
            for reactant, amount in cur_recipe.items():
                cur_chemicals[reactant] += reaction_count * amount
                if reactant != 'ORE':
                    to_reduce.add(reactant)

        process.append(('ORE', cur_chemicals['ORE']))
        process.reverse()

        return process

    def min_ore(self, product: str) -> int:
        return self.min_process(product)[0][1]

    def perform_process(self, process: Sequence[tuple[str, int]], cur_chemicals: dict[str, int]) -> int:
        ore_consumed: int = 0
        for product, num_needed in process[1:-1]:
            if cur_chemicals[product] >= num_needed:
                continue

            difference: int = num_needed - cur_chemicals[product]
            reactions_required: int = difference // self.num_produced[product]
            if difference % self.num_produced[product] != 0:
                reactions_required += 1

            # Perform reaction
            cur_recipe: dict[str, int] = self.recipe[product]
            for reactant, amount in cur_recipe.items():
                if reactant == 'ORE':
                    ore_consumed += amount * reactions_required
                else:
                    # assert cur_chemicals[reactant] >= amount * reactions_required
                    cur_chemicals[reactant] -= amount * reactions_required
            cur_chemicals[product] += self.num_produced[product] * reactions_required

        # Perform final reaction
        product = process[-1][0]
        cur_recipe: dict[str, int] = self.recipe[product]
        for reactant, amount in cur_recipe.items():
            if reactant == 'ORE':
                ore_consumed += amount
            else:
                assert cur_chemicals[reactant] >= amount
                cur_chemicals[reactant] -= amount
        cur_chemicals[product] += self.num_produced[product]

        return ore_consumed

    def max_producible(self, product: str, ore_available: int) -> int:
        cur_chemicals: dict[str, int] = {chemical: 0 for chemical in self.recipe}
        product_process: list[tuple[str, int]] = self.min_process(product)

        while True:
            ore_consumed: int = self.perform_process(product_process, cur_chemicals)
            if ore_consumed > ore_available:
                return cur_chemicals[product] - self.num_produced[product]

            ore_available -= ore_consumed


def part1(data):
    """Solve part 1"""
    factory: Nanofactory = Nanofactory(data)
    return factory.min_ore('FUEL')


def part2(data):
    """Solve part 2"""
    factory: Nanofactory = Nanofactory(data)
    # ore, _ = factory.ore_required('FUEL')
    # print(ore)
    return factory.max_producible('FUEL', 1000000000000)


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
