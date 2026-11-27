from collections import deque
from dataclasses import dataclass
from enum import Enum, auto, unique


@unique
class PDAState(Enum):
    START = auto()
    INNER = auto()
    ACCEPT = auto()


@dataclass(frozen=True, slots=True)
class Transition:
    state: PDAState
    push: tuple[str, ...] = ()


type TransitionKey = tuple[PDAState, str | None, str]
type Stack = tuple[str, ...]
type Configuration = tuple[PDAState, int, Stack]


class PDA:
    def __init__(
        self,
        transitions: dict[TransitionKey, tuple[Transition, ...]],
        alphabet: set[str],
        stack_bottom: str = "$",
        max_configurations: int = 100_000,
    ) -> None:
        if len(stack_bottom) != 1:
            raise ValueError("Stack bottom must be one character.")
        if max_configurations < 1:
            raise ValueError("Configuration limit must be positive.")

        self._transitions = transitions.copy()
        self._alphabet = frozenset(alphabet)
        self._stack_bottom = stack_bottom
        self._max_configurations = max_configurations

    def check(self, text: str, verbose: bool = False) -> bool:
        if not set(text) <= self._alphabet:
            return False

        initial: Configuration = (PDAState.START, 0, (self._stack_bottom,))

        queue = deque([initial])
        visited = {initial}

        while queue:
            state, pos, stack = queue.popleft()

            if verbose:
                print(f"State: {state.name}, input: {text[pos:]!r}, stack: {''.join(stack)!r}")

            if state == PDAState.ACCEPT and pos == len(text):
                return True

            if not stack:
                continue

            top, rest = stack[0], stack[1:]
            symbols = (None, text[pos]) if pos < len(text) else (None,)

            for symbol in symbols:
                for transition in self._transitions.get((state, symbol, top), ()):
                    next_pos = pos if symbol is None else pos + 1
                    next_stack = transition.push + rest

                    config = (
                        transition.state,
                        next_pos,
                        next_stack,
                    )

                    if config in visited:
                        continue

                    if len(visited) >= self._max_configurations:
                        raise RuntimeError("Configuration limit exceeded.")

                    visited.add(config)
                    queue.append(config)

        return False
