import typing
import math


class Cube(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def distance(self, start: 'Cube' = None) -> float:
        if start is None:
            start = ORIGIN

        return math.sqrt((self.x - start.x) ** 2 + (self.y - start.y) ** 2 + (self.z - start.z) ** 2)

    def manhattan_distance(self, start: 'Cube' = None) -> int:
        if start is None:
            start = ORIGIN

        return abs(self.x - start.x) + abs(self.y - start.y) + abs(self.z - start.z)


ORIGIN: Cube = Cube(0, 0, 0)
