import typing
import math

CubeTuple: typing.TypeAlias = tuple[int, ...]


class Cube(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    def distance(self, start: CubeTuple = (0, 0, 0)) -> float:
        start = Cube(*start)
        return math.hypot(self.x - start.x, self.y - start.y, self.z - start.z)

    def manhattan_distance(self, start: CubeTuple = (0, 0, 0)) -> int:
        start = Cube(*start)
        return abs(self.x - start.x) + abs(self.y - start.y) + abs(self.z - start.z)


ORIGIN: Cube = Cube(0, 0, 0)
