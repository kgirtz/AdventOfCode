from collections.abc import Hashable, Callable
from typing import TypeVar

_T: TypeVar = TypeVar('_T', bound=Hashable)


def iterate_state(initial_state: _T, num_iterations: int, transformation: Callable[[_T], _T]) -> _T:
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
