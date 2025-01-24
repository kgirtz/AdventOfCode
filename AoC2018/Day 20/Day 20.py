import pathlib
import sys
import os

from xypair import XYpair, ORIGIN


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.strip().strip('^$')


rooms: dict[XYpair, int] = {}


def update_room(room: XYpair, doors: int) -> None:
    if room not in rooms or doors < rooms[room]:
        rooms[room] = doors


def move(cur_pos: XYpair, direction: str) -> XYpair:
    match direction:
        case 'N':
            return cur_pos.up(2)
        case 'S':
            return cur_pos.down(2)
        case 'E':
            return cur_pos.right(2)
        case 'W':
            return cur_pos.left(2)


def longest_match(regex: str, start: XYpair = ORIGIN, doors_so_far: int = 0) -> None:
    cur_room: XYpair = start
    cur_pos: int = doors_so_far
    while True:
        # Search for first open paren
        i: int = cur_pos
        if i == len(regex):
            return

        while regex[i] != '(':
            update_room(cur_room, i)
            cur_room = move(cur_room, regex[i])
            i += 1
            if i == len(regex):
                return

        # Skip open paren
        cur_pos = i + 1

        # Find matching close paren and vertical bars
        i = cur_pos
        num_open: int = 0
        bars: list[int] = []
        while num_open > 0 or regex[i] != ')':
            if regex[i] == '(':
                num_open += 1
            elif regex[i] == ')':
                num_open -= 1
            elif regex[i] == '|' and num_open == 0:
                bars.append(i)
            i += 1

        # Split options
        start_of_options: int = cur_pos
        options: list[str] = []
        for bar in bars:
            options.append(regex[cur_pos:bar])
            cur_pos = bar + 1
        options.append(regex[cur_pos:i])

        # Calculate longest option, unless options are detours
        for option in options:
            if option:
                longest_match(option, cur_room, start_of_options)

        # Skip close paren
        cur_pos = i + 1


"""def longest_match(regex: str) -> int:
    cur_pos: int = 0
    longest: int = 0
    while True:
        # Search for first open paren
        i: int = regex.find('(', cur_pos)
        if i == -1:
            return longest + len(regex[cur_pos:])

        # Add fixed string to length
        longest += i - cur_pos

        # Skip open paren
        cur_pos = i + 1

        # Find matching close paren and vertical bars
        i = cur_pos
        num_open: int = 0
        bars: list[int] = []
        while num_open > 0 or regex[i] != ')':
            if regex[i] == '(':
                num_open += 1
            elif regex[i] == ')':
                num_open -= 1
            elif regex[i] == '|' and num_open == 0:
                bars.append(i)
            i += 1

        # Split options
        options: list[str] = []
        for bar in bars:
            options.append(regex[cur_pos:bar])
            cur_pos = bar + 1
        options.append(regex[cur_pos:i])

        # Calculate longest option, unless options are detours
        if all(options):  # TODO: could miss longest path at end of a detour
            longest += max(longest_match(option) for option in options)

        # Skip close paren
        cur_pos = i + 1"""


def part1(data):
    """Solve part 1"""
    return longest_match(data)


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 18
    PART2_TEST_ANSWER = None

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
