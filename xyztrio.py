import typing
import math
import functools
import collections.abc

XYZtuple: typing.TypeAlias = tuple[int, ...]


def accept_tuple(func: collections.abc.Callable) -> collections.abc.Callable:
    @functools.wraps(func)
    def wrapper(trio_or_tuple: XYZtuple, *args, **kwargs):
        return func(XYZtrio(*trio_or_tuple), *args, **kwargs)
    return wrapper


def accept_tuple_method(func: collections.abc.Callable) -> collections.abc.Callable:
    @functools.wraps(func)
    def wrapper(self, trio_or_tuple: XYZtuple, *args, **kwargs):
        return func(self, XYZtrio(*trio_or_tuple), *args, **kwargs)
    return wrapper


@typing.final
class XYZtrio(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    @accept_tuple_method
    def distance(self, start: typing.Self) -> float:
        return math.hypot(self.x - start.x, self.y - start.y, self.z - start.z)

    @accept_tuple_method
    def manhattan_distance(self, start: typing.Self) -> int:
        return abs(self.x - start.x) + abs(self.y - start.y) + abs(self.z - start.z)

    def __add__(self, other: XYZtuple) -> typing.Self:
        if isinstance(other, tuple):
            other = XYZtrio(*other)
            return XYZtrio(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __radd__(self, other: typing.Any) -> typing.Self:
        return self + other

    def __sub__(self, other: XYZtuple) -> typing.Self:
        if isinstance(other, tuple):
            other = XYZtrio(*other)
            return XYZtrio(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __rsub__(self, other: XYZtuple) -> XYZtuple:
        if isinstance(other, tuple):
            other = XYZtrio(*other)
            return other.x - self.x, other.y - self.y, other.z - self.z
        return NotImplemented

    def __mul__(self, other: int) -> typing.Self:
        if isinstance(other, int):
            return XYZtrio(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other: typing.Any) -> typing.Self:
        return self * other

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return self * -1

    def __abs__(self) -> float:
        return self.distance(ORIGIN)


ORIGIN: XYZtrio = XYZtrio(0, 0, 0)
