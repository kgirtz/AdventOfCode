import collections

import xypair


class Space:
    def __init__(self,
                 space_str: str | collections.abc.Sequence[str],
                 item_types: collections.abc.Container[str] = tuple(),
                 *,
                 default: str = '.') -> None:

        if isinstance(space_str, str):
            space_str = space_str.split('\n')
        else:
            space_str = list(space_str)

        self.height: int = len(space_str)
        self.width: int = max(len(s) for s in space_str)
        self.items: dict[str, set[xypair.XYpair]] = collections.defaultdict(set)
        self.integer_values: bool = False
        self.default: str = default

        for y, line in enumerate(space_str):
            for x, tile in enumerate(line):
                if (not item_types and tile != self.default) or tile in item_types:
                    self.items[tile].add(xypair.XYpair(x, y))
        self.items = dict(self.items)

    def __str__(self) -> str:
        lines: list[str] = []
        for y in range(self.height):
            line: str = ''
            for x in range(self.width):
                value: str = self.default
                for item, pts in self.items.items():
                    if (x, y) in pts:
                        value = item
                        break
                line += value
            lines.append(line)
        return '\n'.join(lines)

    def __getitem__(self, pt: xypair.XYtuple) -> str:
        value: str = self.default
        for item, pts in self.items.items():
            if pt in pts:
                value = item
                break

        return int(value) if self.integer_values else value

    @xypair.accept_tuple_method
    def in_space(self, pt: xypair.XYpair) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def on_edge(self, pt: xypair.XYtuple) -> bool:
        return self.on_top_edge(pt) or self.on_bottom_edge(pt) or self.on_left_edge(pt) or self.on_right_edge(pt)

    @staticmethod
    @xypair.accept_tuple
    def on_top_edge(pt: xypair.XYpair) -> bool:
        return pt.y == 0

    @xypair.accept_tuple_method
    def on_bottom_edge(self, pt: xypair.XYpair) -> bool:
        return pt.y == self.height - 1

    @staticmethod
    @xypair.accept_tuple
    def on_left_edge(pt: xypair.XYpair) -> bool:
        return pt.x == 0

    @xypair.accept_tuple_method
    def on_right_edge(self, pt: xypair.XYpair) -> bool:
        return pt.x == self.width - 1

    @xypair.accept_tuple_method
    def neighbors(self, pt: xypair.XYpair, *args, **kwargs) -> set[xypair.XYpair]:
        return {n for n in pt.neighbors(*args, **kwargs) if self.in_space(n)}

    def surrounding(self, center: xypair.XYtuple, radius: int) -> set[xypair.XYpair]:
        surrounding: set[xypair.XYtuple] = set()
        edge: set[xypair.XYtuple] = {center}
        for _ in range(radius):
            surrounding.update(edge)
            new_edge: set[xypair.XYtuple] = set()
            for e in edge:
                new_edge.update(self.neighbors(e))
            edge = new_edge - surrounding

        surrounding.remove(center)
        return {xypair.XYpair(x, y) for x, y in surrounding}

    def initial_position(self, item: str) -> xypair.XYpair:
        pts: list[xypair.XYpair] = list(self.items[item])
        if len(pts) > 1:
            raise ValueError(f"more than one {item} found")
        return pts.pop()

    def blockers(self, *, exclude: collections.abc.Container[str] = tuple()) -> set[xypair.XYpair]:
        blockers: set[xypair.XYpair] = set()
        for k, v in self.items.items():
            if k not in exclude:
                blockers.update(v)
        return blockers

    def reachable(self,
                  start: xypair.XYtuple,
                  targets: collections.abc.Iterable[xypair.XYtuple],
                  *,
                  nonblockers: collections.abc.Container[str] = tuple()) \
            -> set[xypair.XYpair]:

        results: dict[xypair.XYpair, tuple[int, list[xypair.XYpair]]] \
            = self.__find_points(start, targets, nonblockers)

        return set(results.keys())

    def reachable_in_fewest_steps(self,
                                  start: xypair.XYtuple,
                                  targets: collections.abc.Iterable[xypair.XYtuple],
                                  *,
                                  nonblockers: collections.abc.Container[str] = tuple()) \
            -> (set[xypair.XYpair], int):

        results: dict[xypair.XYpair, tuple[int, list[xypair.XYpair]]] \
            = self.__find_points(start, targets, nonblockers, stop_at_nearest=True)

        return set(results.keys()), (results.popitem()[1][0] if results else -1)

    def shortest_path_lengths(self,
                              start: xypair.XYtuple,
                              targets: collections.abc.Iterable[xypair.XYtuple],
                              *,
                              nonblockers: collections.abc.Container[str] = tuple()) \
            -> dict[xypair.XYpair, int]:

        results: dict[xypair.XYpair, tuple[int, list[xypair.XYpair]]] \
            = self.__find_points(start, targets, nonblockers)

        return {k: d for k, (d, _) in results.items()}

    def min_paths(self,
                  start: xypair.XYtuple,
                  targets: collections.abc.Iterable[xypair.XYtuple],
                  *,
                  nonblockers: collections.abc.Container[str] = tuple()) \
            -> dict[xypair.XYpair, set[tuple[xypair.XYpair, ...]]]:

        targets = set(targets)
        blockers: set[xypair.XYtuple] = self.blockers(exclude=nonblockers)

        paths: dict[xypair.XYtuple, set[tuple[xypair.XYpair, ...]]] = {}
        edge: dict[xypair.XYtuple, set[tuple[xypair.XYpair, ...]]] = {start: {(xypair.XYpair(*start),)}}
        while edge and not (paths.keys() | edge.keys()) >= targets:
            paths.update(edge)
            new_edge: dict[xypair.XYtuple, set[tuple[xypair.XYpair, ...]]] = collections.defaultdict(set)
            for cur_pt, cur_paths in edge.items():
                for n in self.neighbors(cur_pt) - blockers - paths.keys():
                    new_edge[n].update(p + (xypair.XYpair(*n),) for p in cur_paths)
            edge = new_edge

        return {xypair.XYpair(x, y): p for (x, y), p in (paths | edge).items() if (x, y) in targets}

    def __find_points(self,
                      start: xypair.XYtuple,
                      targets: collections.abc.Iterable[xypair.XYtuple],
                      nonblockers: collections.abc.Container[str] = tuple(),
                      stop_at_nearest: bool = False) \
            -> dict[xypair.XYpair, tuple[int, list[xypair.XYpair]]]:

        targets = frozenset(targets)
        blockers: set[xypair.XYtuple] = self.blockers(exclude=nonblockers)

        found: dict[xypair.XYtuple, tuple[int, list[xypair.XYpair]]] = {}
        edge: dict[xypair.XYtuple, tuple[int, list[xypair.XYpair]]] = {start: (0, [])}
        found.update(edge)
        while edge and not found.keys() >= targets and not (stop_at_nearest and found.keys() & targets):
            new_edge: dict[xypair.XYtuple, tuple[int, list[xypair.XYpair]]] = {}
            for cur_pt, (steps, path_prev) in edge.items():
                for n in self.neighbors(cur_pt) - blockers - found.keys():
                    if n in new_edge:
                        assert new_edge[n][0] == steps + 1
                        new_edge[n][1].append(xypair.XYpair(*cur_pt))
                    else:
                        new_edge[n] = (steps + 1, [xypair.XYpair(*cur_pt)])
            edge = new_edge
            found.update(edge)

        return {xypair.XYpair(x, y): (d, p) for (x, y), (d, p) in found.items() if (x, y) in targets}
