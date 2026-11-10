from typing import Dict, Callable, Set, FrozenSet, List
from NFA import NFAutomaton
from DFA import DFAutomaton
from collections import deque
from collections import defaultdict


def nfa_to_dfa(nfa: NFAutomaton) -> DFAutomaton:
    alphabet = nfa._alphabet

    def move(states: FrozenSet[str], symbol: str) -> Set[str]:
        result: set[str] = set()
        for state in states:
            t_func = nfa._transitions.get(state)
            if t_func is not None:
                targets = t_func(symbol)
                if targets:
                    result.update(targets)
        return result

    def states_to_name(states: FrozenSet[str]) -> str:
        if not states:
            return "∅"
        return "{" + ",".join(sorted(states)) + "}"

    start_set: FrozenSet[str] = frozenset(nfa.epsilon_closure({nfa._start_state}))

    unprocessed: list[FrozenSet[str]] = [start_set]
    unprocessed_set: Set[FrozenSet[str]] = {start_set}

    dfa_transitions: Dict[str, Dict[str, str]] = {}
    processed: Set[FrozenSet[str]] = set()

    dfa_accept_states: set[str] = set()

    while unprocessed:
        current_set = unprocessed.pop()
        if current_set in processed:
            continue

        current_name = states_to_name(current_set)
        processed.add(current_set)
        if current_set & nfa._accept_states:
            dfa_accept_states.add(current_name)

        dfa_transitions[current_name] = {}

        for symbol in alphabet:
            next_set = frozenset(nfa.epsilon_closure(move(current_set, symbol)))
            next_name = states_to_name(next_set)

            if next_set:
                dfa_transitions[current_name][symbol] = next_name
                if next_set not in processed and next_set not in unprocessed_set:
                    unprocessed_set.add(next_set)
                    unprocessed.append(next_set)

    final_transitions: Dict[str, Callable[[str], str | None]] = {}
    for state_name, trans_map in dfa_transitions.items():
        def make_transition(t_map: Dict[str, str]):
            return lambda symbol: t_map.get(symbol)

        final_transitions[state_name] = make_transition(trans_map)

    start_name = states_to_name(start_set)

    return DFAutomaton(
        start_state=start_name,
        accept_states=dfa_accept_states,
        transitions=final_transitions,
        alphabet=alphabet
    )


def minimize_dfa(dfa: DFAutomaton) -> DFAutomaton:
    states = _find_reachable_states(dfa)

    partition = _initial_partition(states, dfa._accept_states)
    partition = _refine_partition(partition, dfa, states)

    return _build_minimized_dfa(partition, dfa, states)


def _find_reachable_states(dfa: DFAutomaton) -> Set[str]:
    reachable = set()
    queue = deque([dfa._start_state])
    while queue:
        state = queue.popleft()
        if state in reachable:
            continue
        reachable.add(state)

        t_func = dfa._transitions.get(state)
        if t_func:
            for symbol in dfa._alphabet:
                next_state = t_func(symbol)
                if next_state and next_state not in reachable:
                    queue.append(next_state)

    return reachable


def _initial_partition(states: Set[str], accept_states: Set[str]) -> List[Set[str]]:
    accepting = states & accept_states
    non_accepting = states - accept_states
    return [s for s in (accepting, non_accepting) if s]


def _refine_partition(
    partition: List[Set[str]],
    dfa: DFAutomaton,
    states: Set[str]
) -> List[Set[str]]:
    changed = True

    while changed:
        changed = False
        new_partition = []

        for block in partition:
            subblocks = _split_block(block, partition, dfa)
            if len(subblocks) > 1:
                changed = True
            new_partition.extend(subblocks)

        partition = new_partition

    return partition


def _split_block(
    block: Set[str],
    partition: List[Set[str]],
    dfa: DFAutomaton
) -> List[Set[str]]:

    state_to_block_idx = {state: idx for idx, b in enumerate(partition) for state in b}

    signatures = defaultdict(set)
    for state in block:
        t_func = dfa._transitions.get(state)
        block_idx = state_to_block_idx[state]

        sig = []
        for symbol in dfa._alphabet:
            next_state = t_func(symbol) if t_func else None
            sig.append(block_idx if next_state is None else state_to_block_idx[next_state])

        signatures[tuple(sig)].add(state)

    return list(signatures.values())


def _build_minimized_dfa(
    partition: List[Set[str]],
    dfa: DFAutomaton,
    states: Set[str]
) -> DFAutomaton:

    block_names: Dict[frozenset[str], str] = {}
    state_to_block: Dict[str, frozenset[str]] = {}
    accept_states = set()

    for block in partition:
        block_frozen = frozenset(block)
        representative = str(sorted(block))
        block_names[block_frozen] = representative

        state_to_block.update({state: block_frozen for state in block})

        if block & dfa._accept_states:
            accept_states.add(representative)

    transitions: Dict[str, Callable[[str], str | None]] = {}

    for block in partition:
        representative = block_names[frozenset(block)]
        sample_state = next(iter(block))
        t_func = dfa._transitions.get(sample_state)

        if t_func is None:
            continue

        t_dict: Dict[str, str] = {
            sym: block_names[state_to_block[n]]
            for sym in dfa._alphabet
            if (n := t_func(sym)) is not None
        }

        transitions[representative] = lambda sym, d=t_dict: d.get(sym)

    return DFAutomaton(
        start_state=block_names[state_to_block[dfa._start_state]],
        accept_states=accept_states,
        transitions=transitions,
        alphabet=dfa._alphabet
    )
