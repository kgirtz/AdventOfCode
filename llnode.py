from collections.abc import Iterator, Generator
from typing import Self, Any


class LLNode:
    __slots__ = ('value', '_prev', '_next')

    def __init__(self, value: Any, *, circular: bool = False) -> None:
        self.value: Any = value
        self._prev: LLNode | None = self if circular else None
        self._next: LLNode | None = self if circular else None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        value_str: str = f'value={self.value}'
        prev_str: str = '' if self._prev is None else f', prev={self._prev.value}'
        next_str: str = '' if self._next is None else f', next={self._next.value}'
        return f'{self.__class__.__name__}({value_str}{prev_str}{next_str})'

    def __iter__(self) -> Iterator[Self]:
        def node_walker() -> Generator[LLNode]:
            cur_node: LLNode | None = self
            while cur_node is not None:
                yield cur_node
                cur_node = cur_node._next

        return node_walker()

    def unlink(self) -> None:
        if self._next is not None:
            self._next._prev = self._prev
        if self._prev is not None:
            self._prev._next = self._next
        self._next = None
        self._prev = None

    def insert_after(self, successor: Self) -> None:
        successor._prev = self
        successor._next = self._next
        if self._next is not None:
            self._next._prev = successor
        self._next = successor

    def insert_before(self, predecessor: Self) -> None:
        predecessor._prev = self._prev
        predecessor._next = self
        if self._prev is not None:
            self._prev._next = predecessor
        self._prev = predecessor

    def prev(self, steps: int = 1, /) -> Self | None:
        if steps == 1:
            return self._prev
        if steps < 0:
            raise IndexError('number of steps cannot be negative')

        cur_node: LLNode = self
        for _ in range(steps):
            if cur_node is None:
                raise IndexError('not enough previous nodes')
            cur_node = cur_node._prev
        return cur_node

    def next(self, steps: int = 1, /) -> Self | None:
        if steps == 1:
            return self._next
        if steps < 0:
            raise IndexError('number of steps cannot be negative')

        cur_node: LLNode = self
        for _ in range(steps):
            if cur_node is None:
                raise IndexError('not enough following nodes')
            cur_node = cur_node._next
        return cur_node
