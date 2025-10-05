from collections import Counter
from typing import List, Literal, Tuple

def solve(part: Literal["a", "b"], input: str) -> int:
    return solve_a(input) if part == "a" else solve_b(input)

def solve_a(input: str) -> int:
    l, r = _parse_input(input)
    l.sort()
    r.sort()
    return sum(map(lambda a, b: abs(a - b), l, r))


def solve_b(input: str) -> int:
    l, r = _parse_input(input)
    counts = Counter(r)
    return sum([id * cnt * counts.get(id, 0) for (id, cnt) in Counter(l).items()])


def _parse_input(input: str) -> Tuple[List[int], List[int]]:
    l: List[int] = []
    r: List[int] = []
    for i in input.splitlines():
        lst = i.split()
        l.append(int(lst[0]))
        r.append(int(lst[1]))
    return (l, r)
