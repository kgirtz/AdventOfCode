import pathlib
import sys
import os
from typing import Union
from functools import cmp_to_key

Tree = list[Union[int, list]]


def parse(puzzle_input):
    """Parse input"""
    return [pair.split('\n') for pair in puzzle_input.split('\n\n')]


def parse_list(pkt: str) -> tuple[Tree, int]:
    lst: Tree = []
    i: int = 0

    # Move past open bracket
    if not pkt.startswith('['):
        print('Bad list!')
    i += 1

    while not pkt[i] == ']':
        match pkt[i]:
            case '[':
                sublist, consumed = parse_list(pkt[i:])
                lst.append(sublist)
                i += consumed
            case ',':
                i += 1
            case d if d.isdigit():
                j: int = i
                while pkt[i].isdigit():
                    i += 1
                lst.append(int(pkt[j:i]))

    # Count closing bracket
    i += 1
    return lst, i


def cmp_lists(left: Tree, right: Tree) -> int:
    for i in range(min(len(left), len(right))):
        if isinstance(left[i], int) and isinstance(right[i], int):
            if left[i] < right[i]:
                return -1
            elif left[i] > right[i]:
                return 1
            else:
                continue

        if isinstance(left[i], int):
            left[i] = [left[i]]
        if isinstance(right[i], int):
            right[i] = [right[i]]

        result: int = cmp_lists(left[i], right[i])
        if result != 0:
            return result

    if len(left) < len(right):
        return -1
    if len(left) == len(right):
        return 0
    if len(left) > len(right):
        return 1


def part1(data):
    """Solve part 1"""
    index_sum: int = 0
    for i, (pkt1_str, pkt2_str) in enumerate(data, 1):
        pkt1, _ = parse_list(pkt1_str)
        pkt2, _ = parse_list(pkt2_str)

        if cmp_lists(pkt1, pkt2) != 1:
            index_sum += i

    return index_sum


def part2(data):
    """Solve part 2"""
    div_pkt1, _ = parse_list('[[2]]')
    div_pkt2, _ = parse_list('[[6]]')

    all_pkts: list[Tree] = [div_pkt1, div_pkt2]

    for pkt1_str, pkt2_str in data:
        pkt1, _ = parse_list(pkt1_str)
        pkt2, _ = parse_list(pkt2_str)
        all_pkts.extend([pkt1, pkt2])

    all_pkts.sort(key=cmp_to_key(cmp_lists))

    # Find dividers
    dpkt1_idx: int = all_pkts.index(div_pkt1) + 1
    dpkt2_idx: int = all_pkts.index(div_pkt2) + 1

    return dpkt1_idx * dpkt2_idx


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
