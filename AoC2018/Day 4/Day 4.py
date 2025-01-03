import pathlib
import sys
import os
import collections
import datetime
from collections.abc import Iterable
from typing import TypeAlias, LiteralString

Event: TypeAlias = tuple[datetime.datetime, str]
GuardEvent: TypeAlias = tuple[datetime.datetime, str, int]

BEGIN_SHIFT: LiteralString = 'begins shift'


def assign_guards_to_events(events: Iterable[Event]) -> list[GuardEvent]:
    events_with_guards: list[GuardEvent] = []
    cur_guard: int = -1
    for dt, e in sorted(events):
        if BEGIN_SHIFT in e:
            cur_guard = int(e.split()[1].lstrip('#'))
            e = BEGIN_SHIFT
        events_with_guards.append((dt, e, cur_guard))
    return events_with_guards


def parse(puzzle_input: str):
    """Parse input"""
    events: list[Event] = []
    for line in puzzle_input.split('\n'):
        date_str, event = line.split(']')
        date: datetime.datetime = datetime.datetime.strptime(date_str, '[%Y-%m-%d %H:%M')
        events.append((date, event.strip()))
    return assign_guards_to_events(events)


def sleep_analysis(guard: int, events: Iterable[GuardEvent]) -> (int, int, int):
    times = [dt for dt, e, g in events if g == guard and e != BEGIN_SHIFT]
    if not times:
        return 0, -1, -1

    minutes_slept: dict[int, int] = collections.defaultdict(int)
    for i in range(0, len(times), 2):
        sleep_time: int = times[i].minute
        wake_time: int = times[i + 1].minute
        for m in range(sleep_time, wake_time):
            minutes_slept[m] += 1

    total_sleep_time: int = sum(minutes_slept.values())
    most_slept_minute: int = max(minutes_slept, key=minutes_slept.get)
    return total_sleep_time, most_slept_minute, minutes_slept[most_slept_minute]


def part1(data):
    """Solve part 1"""
    guards: set[int] = {guard for _, _, guard in data}

    sleepiest_guard: int = -1
    most_minutes: int = 0
    favorite_minute: int = 0
    for guard in guards:
        m, f, _ = sleep_analysis(guard, data)
        if m > most_minutes:
            sleepiest_guard = guard
            most_minutes = m
            favorite_minute = f

    return sleepiest_guard * favorite_minute


def part2(data):
    """Solve part 2"""
    guards: set[int] = {guard for _, _, guard in data}

    sleepiest_guard: int = -1
    most_frequent: int = 0
    favorite_minute: int = 0
    for guard in guards:
        _, f, c = sleep_analysis(guard, data)
        if c > most_frequent:
            sleepiest_guard = guard
            most_frequent = c
            favorite_minute = f

    return sleepiest_guard * favorite_minute


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 240
    PART2_TEST_ANSWER = 4455

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
