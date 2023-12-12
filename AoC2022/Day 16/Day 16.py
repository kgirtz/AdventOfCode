import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    rates: dict[str, int] = {}
    tunnels: dict[str, list[str]] = {}
    for line in puzzle_input.split('\n'):
        tokens: list[str] = line.split()

        name: str = tokens[1]
        rates[name] = int(tokens[4][5:-1])
        tunnels[name] = [valve.strip(',') for valve in tokens[9:]]

    return rates, tunnels


def get_shortest_paths(name: str, neighbors: dict[str, list[str]]) -> dict[str, int]:
    num_nodes: int = len(neighbors)
    paths: dict[str, int] = {}

    num_hops: int = 0
    nodes: set[str] = {name}

    while len(paths) < num_nodes:
        new_nodes: set[str] = set()
        for node in nodes:
            paths[node] = num_hops
            new_nodes |= set(neighbors[node])

        num_hops += 1
        nodes = new_nodes - paths.keys()

    return paths


class Pathfinder:
    def __init__(self, rates: dict[str, int], tunnels: dict[str, list[str]]) -> None:
        self.distance: dict[str, dict[str, int]] = {name: get_shortest_paths(name, tunnels) for name in tunnels}
        self.rates: dict[str, int] = rates

    def max_pressure_released(self, t_left: int, cur_valve: str, valves_to_open: set[str]) -> int:
        # Remove any valves that can't be opened in time
        time_to_open: dict[str, int] = {v: self.distance[cur_valve][v] + 1 for v in valves_to_open}
        for v, t in time_to_open.items():
            if t >= t_left:
                valves_to_open.remove(v)

        if not valves_to_open:
            return 0

        # Ignore any valves that contribute less in total than the maximum rate in one minute
        max_rate: int = max(self.rates[v] for v in valves_to_open)
        valve_pressure: dict[str, int] = {}
        for v in valves_to_open:
            p: int = (t_left - time_to_open[v]) * self.rates[v]
            if p >= max_rate:
                valve_pressure[v] = p

        max_pressure: int = 0
        for v, p in valve_pressure.items():
            following_pressure: int = self.max_pressure_released(t_left - time_to_open[v], v, valves_to_open - {v})
            max_pressure = max(max_pressure, p + following_pressure)

        return max_pressure

    def max_pressure_released_with_elephant(self, t1_left: int, t2_left: int, cur_v1: str, cur_v2: str, valves_to_open: set[str]) -> int:
        # Remove any valves that can't be opened in time
        time_to_open: dict[str, tuple[int, int]] = {v: (self.distance[cur_v1][v] + 1, self.distance[cur_v2][v] + 1) for v in valves_to_open}
        for v, (t1, t2) in time_to_open.items():
            if t1 >= t1_left and t2 >= t2_left:
                valves_to_open.remove(v)

        if not valves_to_open:
            return 0

        if len(valves_to_open) == 1:
            v: str = valves_to_open.pop()
            return max(t1_left - time_to_open[v][0], t2_left - time_to_open[v][1]) * self.rates[v]

        # Ignore any valves that contribute less in total than the maximum rate in one minute
        max_rate: int = max(self.rates[v] for v in valves_to_open)
        valve_pressure1: dict[str, int] = {}
        valve_pressure2: dict[str, int] = {}
        for v in valves_to_open:
            p1: int = (t1_left - time_to_open[v][0]) * self.rates[v]
            p2: int = (t2_left - time_to_open[v][1]) * self.rates[v]
            if p1 >= max_rate:
                valve_pressure1[v] = p1
            if p2 >= max_rate:
                valve_pressure2[v] = p2

        max_pressure: int = 0
        for v1, p1 in valve_pressure1.items():
            for v2, p2 in valve_pressure2.items():
                if v1 == v2:
                    continue

                next_t1_left: int = t1_left - time_to_open[v1][0]
                next_t2_left: int = t2_left - time_to_open[v2][1]

                if next_t1_left > 0 and next_t2_left > 0:
                    following_pressure: int = self.max_pressure_released_with_elephant(next_t1_left, next_t2_left, v1, v2, valves_to_open - {v1, v2})
                    max_pressure = max(max_pressure, p1 + p2 + following_pressure)
                elif next_t1_left > 0:
                    following_pressure: int = self.max_pressure_released(next_t1_left, v1, valves_to_open - {v1})
                    max_pressure = max(max_pressure, p1 + following_pressure)
                elif next_t2_left > 0:
                    following_pressure: int = self.max_pressure_released(next_t2_left, v2, valves_to_open - {v2})
                    max_pressure = max(max_pressure, p2 + following_pressure)

        return max_pressure


def part1(data):
    """Solve part 1"""
    rates, tunnels = data

    valves_to_open: set[str] = {v for v, r in rates.items() if r > 0}
    starting_valve: str = 'AA'
    num_minutes: int = 30

    return Pathfinder(rates, tunnels).max_pressure_released(num_minutes, starting_valve, valves_to_open)


def part2(data):
    """Solve part 2"""
    rates, tunnels = data

    valves_to_open: set[str] = {v for v, r in rates.items() if r > 0}
    starting_valve: str = 'AA'
    num_minutes: int = 30 - 4

    return Pathfinder(rates, tunnels).max_pressure_released_with_elephant(num_minutes, num_minutes, starting_valve, starting_valve, valves_to_open)


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
