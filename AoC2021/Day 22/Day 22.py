import pathlib
import sys
import os
import parse as scanf
from collections import namedtuple

Box = namedtuple('Box', 'x1 x2 y1 y2 z1 z2')


def parse(puzzle_input):
    """Parse input"""
    reboot_steps: list[tuple[str, Box]] = []
    for line in puzzle_input.split('\n'):
        result = scanf.parse('{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}', line)
        status: str = result[0]
        region: Box = Box(*result[1:])
        reboot_steps.append((status, region))
    return reboot_steps


def split_segment(n1: int, n2: int, positions: list[int]) -> list[tuple[int, int]]:
    segments: list[tuple[int, int]] = []
    for pos in sorted(positions):
        segments.append((n1, pos - 1))
        n1 = pos
    segments.append((n1, n2))
    return segments


def split_box(box: Box, plane: str, positions: list[int]) -> list[Box]:
    split_boxes: list[Box] = []
    if plane == 'x':
        for s1, s2 in split_segment(box.x1, box.x2, positions):
            split_boxes.append(Box(s1, s2, box.y1, box.y2, box.z1, box.z2))
        return split_boxes

    if plane == 'y':
        for s1, s2 in split_segment(box.y1, box.y2, positions):
            split_boxes.append(Box(box.x1, box.x2, s1, s2, box.z1, box.z2))
        return split_boxes

    if plane == 'z':
        for s1, s2 in split_segment(box.z1, box.z2, positions):
            split_boxes.append(Box(box.x1, box.x2, box.y1, box.y2, s1, s2))
        return split_boxes


def overlap_x(box1: Box, box2: Box) -> bool:
    return box2.x1 <= box1.x2 and box2.x2 >= box1.x1


def overlap_y(box1: Box, box2: Box) -> bool:
    return box2.y1 <= box1.y2 and box2.y2 >= box1.y1


def overlap_z(box1: Box, box2: Box) -> bool:
    return box2.z1 <= box1.z2 and box2.z2 >= box1.z1


def linear_fragments(boxes: set[Box], region: Box, plane: str) -> tuple[set[Box], set[Box]]:
    nonoverlapping: set[Box] = set()
    overlapping: set[Box] = set()

    for box in boxes:
        if plane == 'x':
            if box.x1 < region.x1 and region.x2 < box.x2:
                extra, overlap, extra1 = split_box(box, plane, [region.x1, region.x2 + 1])
                nonoverlapping.update((extra, extra1))
            elif box.x1 < region.x1:
                extra, overlap = split_box(box, plane, [region.x1])
                nonoverlapping.add(extra)
            elif region.x2 < box.x2:
                overlap, extra = split_box(box, plane, [region.x2 + 1])
                nonoverlapping.add(extra)
            else:
                overlap = box

        elif plane == 'y':
            if box.y1 < region.y1 and region.y2 < box.y2:
                extra, overlap, extra1 = split_box(box, plane, [region.y1, region.y2 + 1])
                nonoverlapping.update((extra, extra1))
            elif box.y1 < region.y1:
                extra, overlap = split_box(box, plane, [region.y1])
                nonoverlapping.add(extra)
            elif region.y2 < box.y2:
                overlap, extra = split_box(box, plane, [region.y2 + 1])
                nonoverlapping.add(extra)
            else:
                overlap = box

        else:
            if box.z1 < region.z1 and region.z2 < box.z2:
                extra, overlap, extra1 = split_box(box, plane, [region.z1, region.z2 + 1])
                nonoverlapping.update((extra, extra1))
            elif box.z1 < region.z1:
                extra, overlap = split_box(box, plane, [region.z1])
                nonoverlapping.add(extra)
            elif region.z2 < box.z2:
                overlap, extra = split_box(box, plane, [region.z2 + 1])
                nonoverlapping.add(extra)
            else:
                overlap = box

        overlapping.add(overlap)

    return nonoverlapping, overlapping


def fragments(box_to_split: Box, region: Box) -> set[Box]:
    nonoverlapping: set[Box] = set()
    overlapping: set[Box] = {box_to_split}

    if overlap_x(box_to_split, region):
        shaved, overlapping = linear_fragments(overlapping, region, 'x')
        nonoverlapping.update(shaved)

    if overlap_y(box_to_split, region):
        shaved, overlapping = linear_fragments(overlapping, region, 'y')
        nonoverlapping.update(shaved)

    if overlap_z(box_to_split, region):
        shaved, overlapping = linear_fragments(overlapping, region, 'z')
        nonoverlapping.update(shaved)

    return nonoverlapping


def execute_step(status: str, region: Box, core: set[Box]) -> None:
    for box in core.copy():
        if overlap_x(box, region) and overlap_y(box, region) and overlap_z(box, region):
            core.remove(box)
            core.update(fragments(box, region))

    if status == 'on':
        core.add(region)


def volume(box: Box) -> int:
    return (box.x2 - box.x1 + 1) * (box.y2 - box.y1 + 1) * (box.z2 - box.z1 + 1)


def in_initialization_area(region: Box) -> bool:
    if region.x1 < -50 or region.x2 > 50:
        return False
    if region.y1 < -50 or region.y2 > 50:
        return False
    if region.z1 < -50 or region.z2 > 50:
        return False
    return True


def part1(data):
    """Solve part 1"""
    data = [(status, region) for status, region in data if in_initialization_area(region)]
    return part2(data)


def part2(data):
    """Solve part 2"""
    reactor_core: set[Box] = set()
    for status, region in data:
        execute_step(status, region, reactor_core)
    return sum(volume(box) for box in reactor_core)


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
