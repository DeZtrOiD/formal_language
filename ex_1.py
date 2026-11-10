from DFA import DFAutomaton
from NFA import NFAutomaton
import string


def init_automaton_ex_1_1() -> DFAutomaton:
    """^[A-Z][a-zA-Z]*$"""
    return DFAutomaton(
        'S0', {'P1'},
        {
            'S0': lambda symbol: 'P1' if symbol.isupper() else None,
            'P1': lambda symbol: 'P1' if symbol.isalpha() else None
        },
        set(string.ascii_letters)
    )


def inint_nfa_ex_1_1() -> NFAutomaton:
    return NFAutomaton(
        'S0', {'P0', 'P3'},
        {
            'S0': lambda symbol:  (
                None if symbol is None else
                {'P1', 'P12'} if symbol.isupper() else
                {'P12'} if symbol.islower() else None
            ),
            'P1': lambda symbol: {'P2'} if symbol is None else None,
            'P12': lambda symbol: None if symbol is None else {'P3'} if symbol.isalpha() else None,
            'P2': lambda symbol: None if symbol is None else {'P0'} if symbol.isupper() else None
        },
        set(string.ascii_letters)
    )


def init_automaton_ex_1_2() -> DFAutomaton:
    """ .*ab$ """
    return DFAutomaton(
        'S0', {'S2'},
        {
            'S0': lambda symbol: 'S1' if symbol == 'a' else 'S0' if symbol == 'b' else None,
            'S1': lambda symbol: 'S1' if symbol == 'a' else 'S2' if symbol == 'b' else None,
            'S2': lambda symbol: 'S1' if symbol == 'a' else 'S0' if symbol == 'b' else None,
            'S3': lambda symbol: 'S3' if symbol == 'a' else 'S3' if symbol == 'b' else None,
            'S4': lambda symbol: 'S4' if symbol == 'a' else 'S2' if symbol == 'b' else None,
        },
        {'a', 'b'}
    )


def inint_nfa_ex_1_2() -> NFAutomaton:
    """ .*ab.* """
    return NFAutomaton(
        'S0', {'S4'},
        {
            'S0': lambda symbol: (
                {'S0a'} if symbol is None else
                {'S1'} if symbol == 'a' else
                {'S0'} if symbol == 'b' else
                None
            ),
            'S0a': lambda symbol: {'S0'} if symbol is None else None,
            'S1': lambda symbol: (
                {'S1a'} if symbol is None else
                {'S1'} if symbol == 'a' else
                None
            ),
            'S1a': lambda symbol: {'S2'} if symbol is None else None,
            'S2': lambda symbol: (
                {'S3'} if symbol == 'b' else
                None
            ),
            'S3': lambda symbol: {'S4'} if symbol is None else None,
            'S4': lambda symbol: {'S4'} if symbol in ('a', 'b') else None,
        },
        {'a', 'b'}
    )
