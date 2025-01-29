import collections

PART1_TEST_ANSWER = 23
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    return puzzle_input.strip(' ^$')


def explore(regex: str) -> (dict[int, int], dict[int, int]):
    # k: number of doors on path
    # v: numbers of paths of length k
    doors_so_far: dict[int, int] = {0: 1}

    # k: number of doors to pass through
    # v: number of rooms reachable at distance k
    rooms: dict[int, int] = collections.defaultdict(int)
    rooms[0] = 1

    cur_idx: int = 0
    loop_count = 0
    while True:
        # Search for first open paren
        open_paren_idx: int = regex.find('(', cur_idx)

        # Update doors and rooms
        doors_traversed: int = (len(regex) if open_paren_idx == -1 else open_paren_idx) - cur_idx
        if doors_traversed:
            for path_len, num_paths in doors_so_far.items():
                for d in range(1, doors_traversed + 1):
                    rooms[path_len + d] += num_paths

            doors_so_far = {path_len + doors_traversed: num_paths for path_len, num_paths in doors_so_far.items()}

        # Return if regex is exhausted
        if open_paren_idx == -1:
            if loop_count > 1:
                print(loop_count, regex)
            return rooms, doors_so_far

        # Skip open paren
        cur_idx = open_paren_idx + 1

        # Find matching close paren and split options
        i: int = cur_idx
        num_open: int = 0
        options: list[str] = []
        while num_open > 0 or regex[i] != ')':
            match regex[i]:
                case '(':
                    num_open += 1
                case ')':
                    num_open -= 1
                case '|':
                    if num_open == 0:
                        options.append(regex[cur_idx:i])
                        cur_idx = i + 1
            i += 1
        options.append(regex[cur_idx:i])

        # Skip close paren
        cur_idx = i + 1

        # Path splits into multiple options
        if all(options):
            new_paths: dict[int, int] = collections.defaultdict(int)
            for option in options:
                opt_rooms, opt_doors = explore(option)

                # Update doors and rooms
                for path_len, num_paths in doors_so_far.items():
                    for d, num_rooms in opt_rooms.items():
                        rooms[path_len + d] += num_paths * num_rooms

                for path_len, num_paths in doors_so_far.items():
                    for d, d_paths in opt_doors.items():
                        new_paths[path_len + d] += num_paths * d_paths
            doors_so_far = new_paths

        # Path takes detours
        else:
            for detour in options:
                if detour:
                    assert '(' not in detour and '|' not in detour and ')' not in detour
                    assert len(detour) % 2 == 0
                    detour_rooms, _ = explore(detour[:len(detour) // 2])

                    # Update rooms only
                    for path_len, num_paths in doors_so_far.items():
                        for d, num_rooms in detour_rooms.items():
                            rooms[path_len + d] += num_paths * num_rooms

        loop_count += 1


def part1(data):
    rooms, _ = explore(data)
    return max(rooms.keys())


def part2(data):  # 10230 is too high
    rooms, _ = explore(data)
    return sum(d for r, d in rooms.items() if r >= 1000)


# ------------- DO NOT MODIFY BELOW THIS LINE ------------- #


import pathlib


def get_puzzle_input(file: pathlib.Path) -> str:
    if not file.exists():
        return ''
    return file.read_text().strip('\n').replace('\t', ' ' * 4)


def execute(func, puzzle_input: str) -> (..., int):
    import time

    start: int = time.perf_counter_ns()
    result = func(parse(puzzle_input))
    execution_time_us: int = (time.perf_counter_ns() - start) // 1000
    return result, execution_time_us


def timestamp(execution_time_us: int) -> str:
    stamp: str = f'{round(execution_time_us / 1000000, 3)} s'
    if execution_time_us < 1000000:
        stamp = f'{round(execution_time_us / 1000, 3)} ms'
    return f'\t[{stamp}]'


def test(part_num: int, directory: str) -> None:
    if part_num == 1:
        func = part1
        answer = PART1_TEST_ANSWER
    else:
        func = part2
        answer = PART2_TEST_ANSWER

    prefix: str = f'PART {part_num} TEST: '
    if answer is None:
        print(prefix + 'skipped')
        return

    file: pathlib.Path = pathlib.Path(directory, f'part{part_num}_test.txt')
    if not file.exists():
        file = pathlib.Path(directory, 'test.txt')

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    result = 'PASS' if result == answer else 'FAIL'
    print(prefix + result + timestamp(duration))


def solve(part_num: int, directory: str) -> None:
    func = part1 if part_num == 1 else part2
    prefix: str = f'PART {part_num}: '

    file: pathlib.Path = pathlib.Path(directory, 'input.txt')
    if not file.exists():
        # Download file?
        ...

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    suffix: str = '' if result is None else timestamp(duration)
    print(prefix + str(result) + suffix)


if __name__ == '__main__':
    import os

    working_directory: str = os.path.dirname(__file__)

    test(1, working_directory)
    test(2, working_directory)
    print()
    solve(1, working_directory)
    solve(2, working_directory)
