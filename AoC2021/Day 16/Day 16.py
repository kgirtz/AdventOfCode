import pathlib
import sys
import os


class Packet:
    def __init__(self, version: int, type_id: int) -> None:
        self.version: int = version
        self.type_id: int = type_id
        self.value: int = 0
        self.sub_packets: list[Packet] = []

    def __str__(self) -> str:
        if self.type_id == 4:
            return f'Literal: {self.value}'
        else:
            op_str: str = f'Operator: {self.type_id}'
            for sp in self.sub_packets:
                op_str += f'\n\t{str(sp)}'
            return op_str


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def hex_to_bin(packet: str) -> str:
    binary_list: list[str] = []
    for nibble in packet:
        binary_list.append(f'{int(nibble, 16):04b}')
    return ''.join(binary_list)


def parse_literal(packet: Packet, stream: str) -> str:
    nibbles: list[str] = []
    while stream[0] == '1':
        nibbles.append(stream[1:5])
        stream = stream[5:]
    nibbles.append(stream[1:5])
    stream = stream[5:]

    packet.value = int(''.join(nibbles), 2)
    return stream


def evaluate(operation: int, sub_packets: list[Packet]) -> int:
    if operation == 0:
        return sum(p.value for p in sub_packets)
    if operation == 1:
        product: int = sub_packets[0].value
        for p in sub_packets[1:]:
            product *= p.value
        return product
    if operation == 2:
        return min(p.value for p in sub_packets)
    if operation == 3:
        return max(p.value for p in sub_packets)
    if operation == 5:
        return int(sub_packets[0].value > sub_packets[1].value)
    if operation == 6:
        return int(sub_packets[0].value < sub_packets[1].value)
    if operation == 7:
        return int(sub_packets[0].value == sub_packets[1].value)


def parse_operator(packet: Packet, stream: str) -> str:
    length_type_id: str = stream[0]
    if length_type_id == '0':
        sub_packets_length: int = int(stream[1:16], 2)
        stream = stream[16:]
        remaining_length: int = len(stream) - sub_packets_length
        while len(stream) > remaining_length:
            sub_packet, stream = parse_packet(stream)
            packet.sub_packets.append(sub_packet)

    else:
        num_sub_packets: int = int(stream[1:12], 2)
        stream = stream[12:]
        for _ in range(num_sub_packets):
            sub_packet, stream = parse_packet(stream)
            packet.sub_packets.append(sub_packet)

    packet.value = evaluate(packet.type_id, packet.sub_packets)

    return stream


def parse_packet(stream: str) -> tuple[Packet, str]:
    version: int = int(stream[:3], 2)
    type_id: int = int(stream[3:6], 2)
    stream = stream[6:]
    p: Packet = Packet(version, type_id)

    if type_id == 4:
        stream = parse_literal(p, stream)
    else:
        stream = parse_operator(p, stream)

    return p, stream


def parse_stream(stream: str) -> list[Packet]:
    stream = hex_to_bin(stream)
    packets: list[Packet] = []
    while '1' in stream[:3]:
        packet, stream = parse_packet(stream)
        packets.append(packet)
    return packets


def version_sum(packet: Packet) -> int:
    total: int = 0
    for sp in packet.sub_packets:
        total += version_sum(sp)
    return total + packet.version


def part1(data):
    """Solve part 1"""
    results: list = []
    for line in data:
        packets: list[Packet] = parse_stream(line)
        results.append(sum(version_sum(p) for p in packets))
    return results


def part2(data):
    """Solve part 2"""
    results: list = []
    for line in data:
        packets: list[Packet] = parse_stream(line)
        results.append(packets[0].value)
    return results


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
