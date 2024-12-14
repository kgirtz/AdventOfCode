import typing
import math
import functools

CubeTuple: typing.TypeAlias = tuple[int, ...]


def accept_tuple(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrapper(cube_or_tuple: CubeTuple, *args, **kwargs):
        return func(Cube(*cube_or_tuple), *args, **kwargs)
    return wrapper


def accept_tuple_method(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrapper(self, cube_or_tuple: CubeTuple, *args, **kwargs):
        return func(self, Cube(*cube_or_tuple), *args, **kwargs)
    return wrapper


@typing.final
class Cube(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    def __bool__(self) -> bool:
        return self != ORIGIN

    @accept_tuple_method
    def distance(self, start: typing.Self) -> float:
        return math.hypot(self.x - start.x, self.y - start.y, self.z - start.z)

    @accept_tuple_method
    def manhattan_distance(self, start: typing.Self) -> int:
        return abs(self.x - start.x) + abs(self.y - start.y) + abs(self.z - start.z)

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return Cube(-self.x, -self.y, -self.z)

    def __abs__(self) -> float:
        return self.distance(ORIGIN)


ORIGIN: Cube = Cube(0, 0, 0)
