
PART1_TEST_ANSWER = None
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    config, *state_strs = puzzle_input.split('\n\n')
    initial_state: str = config.split('\n')[0].split()[-1].rstrip('.')
    num_steps: int = int(config.split()[-2])

    states: dict[str, list[tuple[int, int, str]]] = {}
    for state_str in state_strs:
        lines: list[str] = state_str.split('\n')
        name: str = lines[0][-2]
        lines = lines[1:]
        actions: list[tuple[int, int, str]] = []
        for v in range(2):
            v *= 4
            value: int = int(lines[v + 1].split()[-1].rstrip('.'))
            direction: int = -1 if lines[v + 2].split()[-1] == 'left.' else 1
            next_state: str = lines[v + 3].split()[-1].rstrip('.')
            actions.append((value, direction, next_state))
        states[name] = actions

    return initial_state, num_steps, states


def part1(data):
    cur_state, num_steps, states = data

    ones: set[int] = set()
    cur_pos: int = 0
    for _ in range(num_steps):
        cur_value: int = int(cur_pos in ones)
        new_value, direction, cur_state = states[cur_state][cur_value]
        if new_value == 1:
            ones.add(cur_pos)
        else:
            ones.discard(cur_pos)

        cur_pos += direction

    return len(ones)


def part2(data):
    return None


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
    #test(2, working_directory)
    print()
    solve(1, working_directory)
    #solve(2, working_directory)
