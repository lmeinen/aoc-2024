from __future__ import annotations
from functools import cache, reduce
from typing import Literal

from util.models import Coordinate, Size


def solve(part: Literal["a", "b"], input: str) -> int:
    stones = [[int(d) for d in i] for i in input.split()]

    def blink(stone: list[int]) -> list[list[int]]: ...

    for _ in range(25):
        ...
    return len(stones)
