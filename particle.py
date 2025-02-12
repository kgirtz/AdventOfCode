import typing

import aoctools
from xypair import XYpair, XYtuple
from xyztrio import XYZtrio, XYZtuple


class Particle2D:
    def __init__(self, position: XYtuple, velocity: XYtuple, acceleration: XYtuple = (0, 0)) -> None:
        self.position: XYpair = XYpair(*position)
        self.velocity: XYpair = XYpair(*velocity)
        self.acceleration: XYpair = XYpair(*acceleration)

    def __hash__(self) -> int:
        return hash((self.position, self.velocity, self.acceleration))

    def __eq__(self, other: typing.Self) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: typing.Self) -> bool:
        return abs(self.position) < abs(other.position)

    def position_at_time(self, t: int) -> XYpair:
        return self.position + self.velocity * t + self.acceleration * (t * (t + 1) // 2)

    def velocity_at_time(self, t: int) -> XYpair:
        return self.velocity + self.acceleration * t

    def tick(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity

    def collision_time(self, other: typing.Self) -> int:
        """ Return time of first collision, -1 indicates no collision occurs """

        # a(t) = a0
        # v(t) = v0 + a(t)t = v0 + a0t
        # p(t) = p0 + v(t)t = p0 + v0t + a0t(t + 1)/2
        #
        # collision: p1(t) = p2(t) for t > 0
        # p1 + v1t + a1t(t + 1)/2 = p2 + v2t + a2t(t + 1)/2
        # 2(p1 - p2) + 2(v1 - v2)t + (a1 - a2)t(t + 1) = 0
        # 2dp + 2dvt + dat^2 + dat = 0
        # 2dp + (2dv + da)t + dat^2 = 0

        delta_p: XYpair = self.position - other.position
        delta_v: XYpair = self.velocity - other.velocity
        delta_a: XYpair = self.acceleration - other.acceleration

        x_roots: tuple[int | None, ...] = aoctools.quadratic_roots_int(delta_a.x, 2 * delta_v.x + delta_a.x, 2 * delta_p.x)
        y_roots: tuple[int | None, ...] = aoctools.quadratic_roots_int(delta_a.y, 2 * delta_v.y + delta_a.y, 2 * delta_p.y)

        for i in range(2):
            t_values: set[int | None] = set()
            if delta_p.x or delta_v.x or delta_a.x:
                t_values.add(x_roots[i])
            if delta_p.y or delta_v.y or delta_a.y:
                t_values.add(y_roots[i])

            if len(t_values) == 1:
                t: int = t_values.pop()
                if t is not None and t >= 0:
                    return t

        return -1


class Particle3D:
    def __init__(self, position: XYZtuple, velocity: XYZtuple, acceleration: XYZtuple = (0, 0, 0)) -> None:
        self.position: XYZtrio = XYZtrio(*position)
        self.velocity: XYZtrio = XYZtrio(*velocity)
        self.acceleration: XYZtrio = XYZtrio(*acceleration)
    
    def __hash__(self) -> int:
        return hash((self.position, self.velocity, self.acceleration))

    def __eq__(self, other: typing.Self) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: typing.Self) -> bool:
        return abs(self.position) < abs(other.position)

    def position_at_time(self, t: int) -> XYZtrio:
        return self.position + self.velocity * t + self.acceleration * (t * (t + 1) // 2)

    def velocity_at_time(self, t: int) -> XYZtrio:
        return self.velocity + self.acceleration * t
    
    def tick(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity

    def collision_time(self, other: typing.Self) -> int:
        """ Return time of first collision, -1 indicates no collision occurs """

        # a(t) = a0
        # v(t) = v0 + a(t)t = v0 + a0t
        # p(t) = p0 + v(t)t = p0 + v0t + a0t(t + 1)/2
        #
        # collision: p1(t) = p2(t) for t > 0
        # p1 + v1t + a1t(t + 1)/2 = p2 + v2t + a2t(t + 1)/2
        # 2(p1 - p2) + 2(v1 - v2)t + (a1 - a2)t(t + 1) = 0
        # 2dp + 2dvt + dat^2 + dat = 0
        # 2dp + (2dv + da)t + dat^2 = 0

        delta_p: XYZtrio = self.position - other.position
        delta_v: XYZtrio = self.velocity - other.velocity
        delta_a: XYZtrio = self.acceleration - other.acceleration

        x_roots: tuple[int | None, ...] = aoctools.quadratic_roots_int(delta_a.x, 2 * delta_v.x + delta_a.x, 2 * delta_p.x)
        y_roots: tuple[int | None, ...] = aoctools.quadratic_roots_int(delta_a.y, 2 * delta_v.y + delta_a.y, 2 * delta_p.y)
        z_roots: tuple[int | None, ...] = aoctools.quadratic_roots_int(delta_a.z, 2 * delta_v.z + delta_a.z, 2 * delta_p.z)

        for i in range(2):
            t_values: set[int | None] = set()
            if delta_p.x or delta_v.x or delta_a.x:
                t_values.add(x_roots[i])
            if delta_p.y or delta_v.y or delta_a.y:
                t_values.add(y_roots[i])
            if delta_p.z or delta_v.z or delta_a.z:
                t_values.add(z_roots[i])

            if len(t_values) == 1:
                t: int = t_values.pop()
                if t is not None and t >= 0:
                    return t

        return -1
    