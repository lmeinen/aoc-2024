
from functools import reduce
from typing import List, Literal, Tuple


def solve(part: Literal["a", "b"], input: str) -> int:
    reports = _parse_input(input)
    if part == "a":
        return sum([1 if not _check_unsafe(report) else 0 for report in reports])
    else:
        total = 0
        for report in reports:
            idxs = _check_unsafe(report)
            total += 1 if reduce(lambda safe, idx: safe or not _check_unsafe(report[0:idx] + report[idx  + 1:]), idxs, not idxs) else 0
        return total

def _check_unsafe(report: List[int]) -> List[int]:
    differences = [a - b for (a, b) in zip(report , report[1:])] 
    maxd = max(enumerate(differences), key=lambda t: t[1])
    mind = min(enumerate(differences), key=lambda t: t[1])
    if -3 <= mind[1] <= maxd[1] < 0 or 0 < mind[1] <= maxd[1] <= 3:
        return []
    else:
        return [mind[0], mind[0] + 1, maxd[0], maxd[0] + 1]

def _parse_input(input: str) -> List[List[int]]:
    return [list(map(lambda s: int(s), line.split())) for line in input.splitlines()]