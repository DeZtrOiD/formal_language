from collections import defaultdict


def dechain(nonterminal: set[str], production: dict[str, set[tuple[str, ...]]]) -> dict[str, set[tuple[str, ...]]]:

    def build_cyclic_reachable(start_nt: str) -> set[str]:
        reachable = {start_nt}
        queue = [start_nt]

        while queue:
            current = queue.pop(0)
            if current in production:
                for rule in production[current]:
                    if len(rule) == 1 and rule[0] in nonterminal:
                        next_nt = rule[0]
                        if next_nt not in reachable:
                            reachable.add(next_nt)
                            queue.append(next_nt)

        return reachable

    new_rules: dict[str, set[tuple[str, ...]]] = defaultdict(set)

    list_C_A: list[set[str]] = []
    for A in nonterminal:
        C_A = build_cyclic_reachable(A)
        for B in C_A:
            if any(B in s for s in list_C_A) and len(C_A) == 1:
                continue
            if B in production:
                for rule in production[B]:
                    if len(rule) != 1 or rule[0] not in nonterminal:
                        new_rules[A].add(rule)
        list_C_A.append(C_A)

    return new_rules
