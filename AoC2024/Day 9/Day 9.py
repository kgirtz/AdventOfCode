import pathlib
import sys
import os
from typing import Self, Generator


class Chunk:
    def __init__(self, address: int, length: int, data: int | None = None) -> None:
        self.address: int = address
        self.length: int = length
        self.contents: int | None = data
        self.free_space: int = -1
        self.next: Self | None = None
        self.prev: Self | None = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(addr={self.address}, len={self.length}, file={self.contents})'

    def next_address(self) -> int:
        return self.address + self.length

    def checksum(self) -> int:
        if self.contents is None:
            return 0
        return self.contents * sum(range(self.address, self.next_address()))

    def walk(self) -> Generator[Self, None, None]:
        cur_chunk: Chunk = self
        while cur_chunk is not None:
            yield cur_chunk
            cur_chunk = cur_chunk.next

    def unlink(self) -> None:
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next
            if self.next is None:
                self.prev.free_space = -1
            else:
                self.prev.free_space = self.prev.next.address - self.prev.next_address()
        self.next = None
        self.prev = None
        self.free_space = -1

    def insert_after(self, chunk: Self) -> None:
        # Update chunk
        chunk.next, chunk.prev = self.next, self
        if chunk.next is None:
            chunk.free_space = -1
        else:
            chunk.free_space = chunk.next.address - chunk.next_address()

        # Update self
        self.next = chunk
        self.free_space = self.next.address - self.next_address()

        # Update next
        if chunk.next is not None:
            chunk.next.prev = chunk


class Disk:
    def __init__(self, disk_map: str) -> None:
        self.allocated: Chunk = Chunk(0, int(disk_map[0]), 0)
        self.head: Chunk = self.allocated
        self.tail: Chunk = self.allocated

        cur_addr: int = self.head.length
        for i, len_str in enumerate(disk_map[1:], 1):
            length: int = int(len_str)
            if i % 2 == 0:
                file_id: int = i // 2
                self.allocate(Chunk(cur_addr, length, file_id))
            cur_addr += length

    def allocate(self, chunk: Chunk) -> None:
        self.tail.insert_after(chunk)
        self.tail = chunk

    def filesystem_checksum(self) -> int:
        return sum(chunk.checksum() for chunk in self.allocated.walk())

    def consolidate_memory(self) -> None:
        first_free: Chunk = self.head
        while first_free != self.tail and not first_free.free_space:
            first_free = first_free.next

        while self.tail != first_free:
            if self.tail.length <= first_free.free_space:
                self.tail = self.tail.prev
                chunk: Chunk = self.tail.next
                chunk.unlink()
                chunk.address = first_free.next_address()
                first_free.insert_after(chunk)
            else:
                self.tail.length -= first_free.free_space
                first_free.insert_after(Chunk(first_free.next_address(), first_free.free_space, self.tail.contents))

            while first_free != self.tail and not first_free.free_space:
                first_free = first_free.next

    def consolidate_files(self) -> None:
        first_free: Chunk = self.head
        for i in range(self.tail.contents, 0, -1):
            file_to_move: Chunk = self.tail
            while file_to_move.contents != i:
                file_to_move = file_to_move.prev

            free_chunk: Chunk = first_free
            while free_chunk is not None and free_chunk.free_space < file_to_move.length:
                free_chunk = free_chunk.next
                if free_chunk is not None and free_chunk.address >= file_to_move.address:
                    break

            if free_chunk is None or free_chunk.address >= file_to_move.address:
                continue

            if file_to_move == self.tail and free_chunk != self.tail.prev:
                self.tail = self.tail.prev

            file_to_move.unlink()
            file_to_move.address = free_chunk.next_address()
            free_chunk.insert_after(file_to_move)

            if free_chunk == first_free:
                while first_free != self.tail and not first_free.free_space:
                    first_free = first_free.next


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input.strip()


def part1(data):
    """Solve part 1"""
    disk: Disk = Disk(data)
    disk.consolidate_memory()
    return disk.filesystem_checksum()


def part2(data):
    """Solve part 2"""
    disk: Disk = Disk(data)
    disk.consolidate_files()
    return disk.filesystem_checksum()


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 1928
    PART2_TEST_ANSWER = 2858

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
