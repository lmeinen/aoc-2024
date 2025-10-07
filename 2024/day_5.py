import re
from collections import defaultdict
from typing import Dict, List, Literal, Set


def solve(part: Literal["a", "b"], input: str) -> int:
    partial: Dict[int, Set[int]] = defaultdict(set)
    updates: List[List[int]] = []
    for line in input.splitlines():
        if re.fullmatch(r"\d+\|\d+", line):
            a, b = map(int, line.split("|", 2))
            partial[a].add(b)
        elif re.fullmatch(r"(?:\d+,?)+", line):
            updates.append([int(p) for p in line.split(",")])

    if part == "a":
        total = 0
        for update in updates:
            if _is_sorted(partial, update):
                total += update[len(update) // 2]
        return total
    else:
        total = 0
        for update in updates:
            if not _is_sorted(partial, update):
                sorted = _bubble_sort(partial, update)
                total += sorted[len(sorted) // 2]
        return total


def _is_sorted(rules: Dict[int, Set[int]], order: List[int]) -> bool:
    seen: Set[int] = set()
    for p in order:
        if seen & rules[p]:
            # non-empty intersection: seen pages must be ordered after p
            return False
        seen.add(p)
    return True

def _bubble_sort(rules: Dict[int, Set[int]], order: List[int]) -> List[int]:
    seen: Dict[int, int] = {}
    for i, p in enumerate(order):
        if conflicts := [seen[c] for c in rules[p] if c in seen]:
            order.insert(min(conflicts), order.pop(i))
            return _bubble_sort(rules, order)
        else:
            seen[p] = i
    return order
