from PDAutomaton import PDA, PDAState, Transition

transitions = {
    (PDAState.START, None, "$"): (Transition(PDAState.INNER, ("S", "$")),),
    (PDAState.INNER, "a", "S"): (Transition(PDAState.INNER, ("A", "B")),),
    (PDAState.INNER, "b", "A"): (Transition(PDAState.INNER, ("C",)),),
    (PDAState.INNER, "c", "B"): (Transition(PDAState.INNER, ("A",)),),
    (PDAState.INNER, "d", "C"): (Transition(PDAState.INNER, ("D",)),),
    (PDAState.INNER, "x", "C"): (Transition(PDAState.INNER, ("J",)),),
    (PDAState.INNER, "f", "D"): (Transition(PDAState.INNER, ()),),
    (PDAState.INNER, "b", "J"): (
        Transition(PDAState.INNER, ("J'",)),
        Transition(PDAState.INNER, ()),
    ),
    (PDAState.INNER, "b", "J'"): (
        Transition(PDAState.INNER, ("J'",)),
        Transition(PDAState.INNER, ()),
    ),
    (PDAState.INNER, None, "$"): (Transition(PDAState.ACCEPT, ("$",)),),
}


def init_ex_2() -> PDA:
    return PDA(
        transitions,
        alphabet={"a", "b", "c", "d", "f", "x"},
    )
