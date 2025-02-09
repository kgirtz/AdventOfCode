import math
import typing
import collections.abc

_T: typing.TypeVar = typing.TypeVar('_T', bound=collections.abc.Hashable)


def iterate_state(initial_state: _T, num_iterations: int, transformation: collections.abc.Callable[[_T], _T]) -> _T:
    """ Repeatedly call transformation() on current state, cache results to detect cycles """

    if num_iterations < 0:
        raise ValueError('number of iterations cannot be negative')

    seen: dict[_T, int] = {}
    current_state: _T = initial_state
    for i in range(num_iterations):
        seen[current_state] = i

        current_state = transformation(current_state)

        if current_state in seen:
            startup: int = seen[current_state]
            cycle_length: int = i - startup + 1
            reduced_iterations: int = (num_iterations - startup) % cycle_length
            return iterate_state(current_state, reduced_iterations, transformation)

    return current_state


def linear_roots_int(a: int, b: int) -> int | None:
    """ Solves ax + b = 0 for real, integer roots only """

    if a != 0:
        x: int = round(-b / a)
        if a * x + b == 0:
            return x

    return None


def quadratic_roots_int(a: int, b: int, c: int) -> tuple[int | None, ...]:
    """ Solves ax^2 + bx + c = 0 for real, integer roots only """

    if a == 0:
        linear_root: int | None = linear_roots_int(b, c)
        return linear_root, linear_root

    discriminant: int = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None, None

    integer_roots: list[int | None] = [None, None]
    x: int = round(((-b - math.sqrt(discriminant)) / (2 * a)))
    if a * (x ** 2) + b * x + c == 0:
        integer_roots[0] = x

    x = round((-b + math.sqrt(discriminant)) / (2 * a))
    if a * (x ** 2) + b * x + c == 0:
        integer_roots[1] = x

    return tuple(integer_roots)
