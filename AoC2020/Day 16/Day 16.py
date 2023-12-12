import pathlib
import sys
import os
import parse as scanf
from collections import deque

Range = tuple[int, int]


def parse(puzzle_input):
    """Parse input"""
    fields_str, my_ticket_str, nearby_str = puzzle_input.split('\n\n')

    fields: dict[str, tuple[Range, Range]] = {}
    for line in fields_str.split('\n'):
        field, lo1, hi1, lo2, hi2 = scanf.parse('{}: {:d}-{:d} or {:d}-{:d}', line)
        fields[field] = ((lo1, hi1), (lo2, hi2))

    my_ticket_str = my_ticket_str.split('\n')[1]
    my_ticket: list[int] = [int(n) for n in my_ticket_str.split(',')]

    nearby_lines: list[str] = nearby_str.split('\n')[1:]
    nearby_tickets: list[list[int]] = [[int(n) for n in line.split(',')] for line in nearby_lines]

    return fields, my_ticket, nearby_tickets


def valid_value(value: int, fields: dict[str, tuple[Range, Range]]) -> bool:
    for (lo1, hi1), (lo2, hi2) in fields.values():
        if lo1 <= value <= hi1 or lo2 <= value <= hi2:
            return True
    return False


def valid_ticket(ticket: list[int], fields: dict[str, tuple[Range, Range]]) -> bool:
    for value in ticket:
        if not valid_value(value, fields):
            return False
    return True


def determine_mapping(tickets: list[list[int]], fields: dict[str, tuple[Range, Range]]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    unresolved: deque[int] = deque(range(len(fields)))
    while len(mapping) < len(fields):
        col: int = unresolved.popleft()
        possible: set[str] = {f for f in fields if f not in mapping}
        values: set[int] = {ticket[col] for ticket in tickets}
        invalid: set[str] = set()
        for field in possible:
            (lo1, hi1), (lo2, hi2) = fields[field]
            for value in values:
                if not (lo1 <= value <= hi1 or lo2 <= value <= hi2):
                    invalid.add(field)
                    break

        possible -= invalid
        if len(possible) == 1:
            resolved: str = possible.pop()
            mapping[resolved] = col
        else:
            unresolved.append(col)

    return mapping


def part1(data):
    """Solve part 1"""
    fields, _, nearby_tickets = data
    scanning_error_rate: int = 0
    for ticket in nearby_tickets:
        for value in ticket:
            if not valid_value(value, fields):
                scanning_error_rate += value
    return scanning_error_rate


def part2(data):
    """Solve part 2"""
    fields, my_ticket, nearby_tickets = data
    valid_tickets: list[list[int]] = [t for t in nearby_tickets if valid_ticket(t, fields)] + [my_ticket]
    mapping: dict[str, int] = determine_mapping(valid_tickets, fields)

    product: int = 1
    for field in fields:
        if field.startswith('departure'):
            product *= my_ticket[mapping[field]]
    return product


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
