from typing import Callable, Dict, Set


TransitionFuncDFA = Callable[[str], str | None]


class DFAutomaton:
    def __init__(
            self, start_state: str, accept_states: set[str],
            transitions: Dict[str, TransitionFuncDFA], alphabet: Set[str]):
        self._start_state: str = start_state
        self._accept_states: Set[str] = accept_states
        self._transitions: Dict[str, TransitionFuncDFA] = transitions
        self._alphabet: Set[str] = alphabet

    def check(self, text: str, verbose: bool = True) -> bool:
        if not text and not {self._start_state} & self._accept_states:
            return False

        curr_state: str | None = self._start_state
        if verbose:
            print(f'Start state: {curr_state}, word: {text}')
        for char in text:
            if char not in self._alphabet:
                return False
            if curr_state is None:
                return False
            curr_func = self._transitions.get(curr_state)
            if curr_func is None:
                return False
            old_state = curr_state
            curr_state = curr_func(char)
            if verbose:
                print(f'Old state: {old_state}; char: {char} -> New state: {curr_state}')

        return curr_state in self._accept_states
