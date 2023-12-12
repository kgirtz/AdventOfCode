import pathlib
import sys
import os
import re
from collections import namedtuple
from copy import copy
from typing import Optional

Blueprint = namedtuple('Blueprint', 'ID ore clay obsidian geode')

ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3


def parse(puzzle_input):
    """Parse input"""
    blueprints: list[Blueprint] = []
    for line in puzzle_input.split('\n'):
        nums: list[int] = [int(n) for n in re.findall(r'\d+', line)]
        id_num: int = nums[0]
        ore: int = nums[1]
        clay: int = nums[2]
        obsidian: tuple[int, int] = nums[3], nums[4]
        geode: tuple[int, int] = nums[5], nums[6]
        blueprints.append(Blueprint(id_num, ore, clay, obsidian, geode))

    return blueprints


class State:
    def __init__(self) -> None:
        self.ore: int = 0
        self.clay: int = 0
        self.obsidian: int = 0
        self.geode: int = 0
        self.ore_robots: int = 1
        self.clay_robots: int = 0
        self.obsidian_robots: int = 0
        self.do_not_craft_ore: bool = False
        self.do_not_craft_clay: bool = False
        self.do_not_craft_obsidian: bool = False

    def produce(self) -> None:
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        # geode is produced in bulk when robot is built

    def build(self, robot: int, blueprint: Blueprint, minutes_remaining: int) -> None:
        self.do_not_craft_ore = False
        self.do_not_craft_clay = False
        self.do_not_craft_obsidian = False
        match robot:
            case 0:
                self.ore -= blueprint.ore
                self.ore_robots += 1
            case 1:
                self.ore -= blueprint.clay
                self.clay_robots += 1
            case 2:
                self.ore -= blueprint.obsidian[0]
                self.clay -= blueprint.obsidian[1]
                self.obsidian_robots += 1
            case 3:
                self.ore -= blueprint.geode[0]
                self.obsidian -= blueprint.geode[1]
                self.geode += minutes_remaining  # produce in bulk


class Factory:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint: Blueprint = blueprint
        self.max_ore_robots: int = max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])
        self.max_clay_robots: int = blueprint.obsidian[1]

    def robots_able_to_build(self, s: State) -> set[int]:
        # Always build a geode robot if possible
        if s.ore >= self.blueprint.geode[0] and s.obsidian >= self.blueprint.geode[1]:
            return {GEODE}

        if not s.do_not_craft_obsidian and s.ore >= self.blueprint.obsidian[0] and s.clay >= self.blueprint.obsidian[1]:
            return {OBSIDIAN}

        robots: set[int] = set()
        if not s.do_not_craft_clay and s.ore >= self.blueprint.clay and s.clay_robots < self.max_clay_robots:
            robots.add(CLAY)
        if not s.do_not_craft_ore and s.ore >= self.blueprint.ore and s.ore_robots < self.max_ore_robots:
            robots.add(ORE)
        return robots

    def max_geodes(self, minutes_remaining: int, s: Optional[State] = None) -> int:
        if s is None:
            s = State()

        minutes_remaining -= 1

        # Skip the last minute
        if minutes_remaining == 0:
            return s.geode

        # Create new states for each robot type built
        possible_robots: set[int] = self.robots_able_to_build(s)
        while not possible_robots:
            s.produce()
            minutes_remaining -= 1
            if minutes_remaining == 0:
                return s.geode
            possible_robots = self.robots_able_to_build(s)

        most_geodes: int = 0

        s.produce()
        for new_robot in possible_robots:
            new_state: State = copy(s)
            new_state.build(new_robot, self.blueprint, minutes_remaining)
            most_geodes = max(most_geodes, self.max_geodes(minutes_remaining, new_state))

        # Collect resources on default state
        if ORE in possible_robots:
            s.do_not_craft_ore = True
        if CLAY in possible_robots:
            s.do_not_craft_clay = True
        if OBSIDIAN in possible_robots:
            s.do_not_craft_obsidian = True
        if GEODE not in possible_robots and not (s.do_not_craft_ore and s.do_not_craft_clay and s.do_not_craft_obsidian):
            most_geodes = max(most_geodes, self.max_geodes(minutes_remaining, s))

        return most_geodes


def part1(data):
    """Solve part 1"""
    max_geode_sum: int = 0
    for bp in data:
        geodes: int = Factory(bp).max_geodes(24)
        max_geode_sum += geodes * bp.ID

    return max_geode_sum


def part2(data):
    """Solve part 2"""
    max_geode_product: int = 1
    for bp in data[:3]:
        geodes: int = Factory(bp).max_geodes(32)
        max_geode_product *= geodes

    return max_geode_product


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
