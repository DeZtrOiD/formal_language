from typing import Dict, Callable, Set

TransitionFuncNFA = Callable[[str | None], Set[str] | None]


class NFAutomaton:
    def __init__(
            self, start_state: str, accept_states: Set[str],
            transitions: Dict[str, TransitionFuncNFA], alphabet: Set[str]):
        self._start_state: str = start_state
        self._accept_states: Set[str] = accept_states
        self._transitions: Dict[str, TransitionFuncNFA] = transitions
        self._alphabet: Set[str] = alphabet

    def check(self, text: str, verbose: bool = True):
        curr_states: Set[str] = self.epsilon_closure({self._start_state})
        if not text and not curr_states & self._accept_states:
            return False
        if verbose:
            print(f'Start state (after ε-closure): {curr_states}, word: {text}')
        for char in text:
            if char not in self._alphabet:
                return False

            next_states: set[str] = set()
            for state in curr_states:
                t_func = self._transitions.get(state)
                if t_func is not None:
                    tmp_states = t_func(char)
                    if tmp_states:
                        next_states.update(tmp_states)

            next_states = self.epsilon_closure(next_states)

            if verbose:
                print(f'Old state: {curr_states}; char: {char} -> New state: {next_states}')

            curr_states = next_states
            if not curr_states:
                return False

        return bool(curr_states & self._accept_states)

    def epsilon_closure(self, states: Set[str]) -> set[str]:
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            transition_func = self._transitions.get(state)
            if transition_func is not None:
                epsilon_targets = transition_func(None)
                if epsilon_targets:
                    for target in epsilon_targets:
                        if target not in closure:
                            closure.add(target)
                            stack.append(target)
        return closure
