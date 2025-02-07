from collections.abc import Sequence, Mapping

PART1_TEST_ANSWER = None  # 'baedc'
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    return puzzle_input.strip().split(',')


def dance_move(programs: tuple[str, ...], move: str) -> tuple[str, ...]:
    match move[0]:
        case 's':
            spin_num: int = int(move[1:])
            return programs[-spin_num:] + programs[:-spin_num]

        case 'x':
            pos_a, pos_b = (int(n) for n in move[1:].split('/'))

        case 'p':
            prog_a, prog_b = (n for n in move[1:].split('/'))
            pos_a, pos_b = programs.index(prog_a), programs.index(prog_b)

        case _:
            raise ValueError('invalid dance move')

    new_programs: list[str] = list(programs)
    new_programs[pos_a], new_programs[pos_b] = new_programs[pos_b], new_programs[pos_a]
    return tuple(new_programs)


def initial_program_state(num_programs: int) -> tuple[str, ...]:
    return tuple(chr(ord('a') + i) for i in range(num_programs))


def dance(state: Sequence[str, ...], transform: Mapping[int, int]) -> tuple[str, ...]:
    return tuple(state[transform[i]] for i in range(len(state)))


def iterate_transformation(initial_state: tuple[str, ...], num_iterations: int, transform: Mapping[int, int]) -> tuple[str, ...]:
    seen: dict[..., int] = {}
    state: tuple[str, ...] = initial_state
    for i in range(num_iterations):
        seen[state] = i

        state = dance(state, transform)

        if state in seen:
            startup: int = seen[state]
            cycle_length: int = i - startup + 1
            reduced_minutes: int = (num_iterations - startup) % cycle_length
            return iterate_transformation(state, reduced_minutes, transform)

    return state


def part1(data):
    programs: tuple[str, ...] = initial_program_state(16)  # test = 5, input = 16
    for move in data:
        programs = dance_move(programs, move)
    return ''.join(programs)


def part2(data):  # abkjefdhcgilmnop is not correct
    num_programs: int = 16
    starting_state: tuple[str, ...] = initial_program_state(num_programs)
    programs: tuple[str, ...] = starting_state
    for move in data:
        programs = dance_move(programs, move)

    transformation: dict[int, int] = {programs.index(p): i for i, p in enumerate(starting_state)}
    programs = iterate_transformation(starting_state, 1000000000, transformation)
    return ''.join(programs)


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
