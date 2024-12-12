import typing
import collections

import point


class Space:
    def __init__(self, space_str: str | typing.Sequence[str], item_types: typing.Iterable[str] = tuple(), *, default: str = '.') -> None:
        if isinstance(space_str, str):
            space_str = space_str.split('\n')
        else:
            space_str = list(space_str)

        self.height: int = len(space_str)
        self.width: int = len(space_str[0])
        self.tiles: list[str] = space_str
        self.items: dict[str, set[point.Point]] = collections.defaultdict(set)
        self.integer_values: bool = False
        self.default: str = default

        for y, line in enumerate(space_str):
            for x, tile in enumerate(line):
                if (not item_types and tile != self.default) or tile in item_types:
                    self.items[tile].add(point.Point(x, y))
        self.items = dict(self.items)

    def __str__(self) -> str:
        return '\n'.join(self.tiles)

    @point.accept_tuple
    def __getitem__(self, pt: point.Point) -> str:
        value: str = self.tiles[pt.y][pt.x]
        return int(value) if self.integer_values else value

    @point.accept_tuple
    def valid_point(self, pt: point.Point) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def on_edge(self, pt: point.PointTuple) -> bool:
        return self.on_top_edge(pt) or self.on_bottom_edge(pt) or self.on_left_edge(pt) or self.on_right_edge(pt)

    @staticmethod
    @point.accept_tuple
    def on_top_edge(pt: point.Point) -> bool:
        return pt.y == 0

    @point.accept_tuple
    def on_bottom_edge(self, pt: point.Point) -> bool:
        return pt.y == self.height - 1

    @staticmethod
    @point.accept_tuple
    def on_left_edge(pt: point.Point) -> bool:
        return pt.x == 0

    @point.accept_tuple
    def on_right_edge(self, pt: point.Point) -> bool:
        return pt.x == self.width - 1

    @point.accept_tuple
    def neighbors(self, pt: point.Point, *args, **kwargs) -> set[point.Point]:
        return {n for n in pt.neighbors(*args, **kwargs) if self.valid_point(n)}

    def initial_position(self, value: str) -> point.Point:
        pts: typing.Collection[point.Point] = self.items[value]
        assert len(pts) == 1
        return tuple(pts)[0]
