import typing
import collections

from point import Point, PointTuple


class Space:
    def __init__(self, space_str: str | typing.Sequence[str], item_types: typing.Iterable[str] = tuple(), *, default: str = '.') -> None:
        if isinstance(space_str, str):
            space_str = space_str.split('\n')
        else:
            space_str = list(space_str)

        self.height: int = len(space_str)
        self.width: int = len(space_str[0])
        self.tiles: list[str] = space_str
        self.items: dict[str, set[Point]] = collections.defaultdict(set)
        self.integer_values: bool = False
        self.default: str = default

        for y, line in enumerate(space_str):
            for x, tile in enumerate(line):
                if not item_types or tile in item_types:
                    self.items[tile].add(Point(x, y))
        self.items = dict(self.items)

    def __str__(self) -> str:
        return '\n'.join(self.tiles)

    def __getitem__(self, item: PointTuple) -> str:
        pt = Point(*item)
        value: str = self.tiles[pt.y][pt.x]
        return int(value) if self.integer_values else value

    def valid_point(self, pt: PointTuple) -> bool:
        pt = Point(*pt)
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def on_edge(self, pt: PointTuple) -> bool:
        return self.on_top_edge(pt) or self.on_bottom_edge(pt) or self.on_left_edge(pt) or self.on_right_edge(pt)

    @staticmethod
    def on_top_edge(pt: PointTuple) -> bool:
        return Point(*pt).y == 0

    def on_bottom_edge(self, pt: PointTuple) -> bool:
        return Point(*pt).y == self.height - 1

    @staticmethod
    def on_left_edge(pt: PointTuple) -> bool:
        return Point(*pt).x == 0

    def on_right_edge(self, pt: PointTuple) -> bool:
        return Point(*pt).x == self.width - 1

    def neighbors(self, pt: PointTuple, *args, **kwargs) -> set[Point]:
        return {n for n in Point(*pt).neighbors(*args, **kwargs) if self.valid_point(n)}

    def initial_position(self, value: str) -> Point:
        pts: set[Point] = self.items[value]
        assert len(pts) == 1
        return tuple(pts)[0]
