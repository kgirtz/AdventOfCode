import pathlib
import sys
import os
from typing import Self, Generator
from collections import defaultdict


class Chunk:
    def __init__(self, address: int, length: int, data: int | None = None) -> None:
        self.address: int = address
        self.length: int = length
        self.contents: int | None = data
        self.next: Self | None = None
        self.prev: Self | None = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(addr={self.address}, len={self.length}, file={self.contents})'

    def __eq__(self, other) -> bool:
        return self.address == other.address

    def next_address(self) -> int:
        return self.address + self.length

    def following_free_space(self) -> int:
        if self.next is None:
            return -1
        return self.next.address - self.next_address()

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
        self.next = None
        self.prev = None

    def insert_after(self, chunk: Self) -> None:
        chunk.next, chunk.prev = self.next, self
        self.next = chunk
        if chunk.next is not None:
            chunk.next.prev = chunk


class Disk:
    def __init__(self, disk_map: str) -> None:
        self.allocated: Chunk = Chunk(0, int(disk_map[0]), 0)
        self.head: Chunk = self.allocated
        self.tail: Chunk = self.allocated
        self.first_free_space: Chunk = self.head
        self.free_chunks: dict[int, list[Chunk]] = defaultdict(list)

        cur_addr: int = self.head.length
        for i, len_str in enumerate(disk_map[1:], 1):
            length: int = int(len_str)
            if i % 2 == 0:
                file_id: int = i // 2
                self.allocate(Chunk(cur_addr, length, file_id))
            else:
                self.free_chunks[length].append(self.tail)
            cur_addr += length

    def allocate(self, chunk: Chunk) -> None:
        self.tail.insert_after(chunk)
        self.tail = chunk

    def filesystem_checksum(self) -> int:
        return sum(chunk.checksum() for chunk in self.allocated.walk())

    def update_first_free_space(self) -> None:
        while self.first_free_space != self.tail and not self.first_free_space.following_free_space():
            self.first_free_space = self.first_free_space.next
        """
        for i in self.free_chunks:
            if self.free_chunks[i] and not self.free_chunks[i][0].following_free_space():
                self.free_chunks[i] = self.free_chunks[i][1:]
        for i in self.free_chunks:
            if not self.free_chunks[i]:
                continue
            actual_length: int = self.free_chunks[i][0].length
            if actual_length != i:
                modified_space: Chunk = self.free_chunks[i][0]
                self.free_chunks[i] = self.free_chunks[i][1:]
                self.free_chunks[actual_length].append(modified_space)
                self.free_chunks[actual_length].sort(key=lambda chunk: chunk.address)
        self.first_free_space = min((group[0] for group in self.free_chunks.values()), key=lambda chunk: chunk.address)"""

    def consolidate_memory(self) -> None:
        while self.tail != self.first_free_space:
            free_space_length: int = self.first_free_space.following_free_space()
            if self.tail.length <= free_space_length:
                self.tail = self.tail.prev
                chunk: Chunk = self.tail.next
                chunk.unlink()
                self.first_free_space.insert_after(chunk)
                chunk.address = self.first_free_space.next_address()
            else:
                self.first_free_space.insert_after(Chunk(self.first_free_space.next_address(), free_space_length, self.tail.contents))
                self.tail.length -= free_space_length

            self.update_first_free_space()

    def consolidate_files(self) -> None:
        while self.tail != self.first_free_space:
            free_space_length: int = self.first_free_space.following_free_space()
            if self.tail.length <= free_space_length:
                self.tail = self.tail.prev
                chunk: Chunk = self.tail.next
                chunk.unlink()
                self.first_free_space.insert_after(chunk)
                chunk.address = self.first_free_space.next_address()
            else:
                self.first_free_space.insert_after(
                    Chunk(self.first_free_space.next_address(), free_space_length, self.tail.contents))
                self.tail.length -= free_space_length

            self.update_first_free_space()


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
            ...#assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
