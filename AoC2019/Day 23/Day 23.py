import pathlib
import sys
import os

sys.path.append('..')
from intcode import IntcodeComputer


class Network:
    NAT_ADDR: int = 255

    def __init__(self, num_computers: int, program: list[int]) -> None:
        self.computers: list[IntcodeComputer] = [IntcodeComputer() for _ in range(num_computers)]
        self.nic: list[int] = program
        self.packet_queues: list[list[int]] = [[] for _ in self.computers]
        self.nat: list[int] = []

        # Init all computers
        for addr, comp in enumerate(self.computers):
            comp.execute(self.nic, [addr])

    def send_receive(self, addr: int, rx_packets: list[int]) -> int:
        # Received packets
        if not rx_packets:
            rx_packets.append(-1)
        tx_packets: list[int] = self.computers[addr].run(rx_packets)

        # Sent packets
        for j in range(0, len(tx_packets), 3):
            dst, x, y = tx_packets[j:j + 3]
            if dst == self.NAT_ADDR:
                self.nat = [x, y]
            else:
                self.packet_queues[dst].extend((x, y))

        return len(tx_packets) // 3

    def route_all_computers(self) -> bool:
        idle: bool = not any(self.packet_queues)

        for addr in range(len(self.computers)):
            if self.send_receive(addr, self.packet_queues[addr]) > 0:
                idle = False
            self.packet_queues[addr] = []

        if idle:
            self.send_receive(0, self.nat)

        return idle


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    network: Network = Network(50, data)
    while not network.nat or network.nat[1] < 0:
        network.route_all_computers()
    return network.nat[1]


def part2(data):
    """Solve part 2"""
    network: Network = Network(50, data)

    last_nat_y: int = -1
    while True:
        if network.route_all_computers():
            if network.nat[1] == last_nat_y:
                return last_nat_y
            last_nat_y = network.nat[1]


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
