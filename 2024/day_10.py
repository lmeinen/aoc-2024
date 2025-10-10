from __future__ import annotations
from functools import cache, reduce
from typing import Literal

from util.models import Coordinate, Size


def solve(part: Literal["a", "b"], input: str) -> int:
    grid: list[list[int]] = []
    size = Size(len(grid), len(grid[0]))
    trailheads: set[Coordinate] = set()

    for x, line in enumerate(input.splitlines()):
        heights = list(map(int, line))
        grid.append(heights)
        trailheads |= {
            Coordinate(x, y) for y, height in enumerate(heights) if height == 0
        }

    def height(field: Coordinate) -> int:
        return grid[field.x][field.y]

    def _neighbours(field: Coordinate) -> list[Coordinate]:
        ns = [
            field + (step * sign)
            for sign in [-1, 1]
            for step in [Coordinate(0, 1), Coordinate(1, 0)]]
        return list(filter(lambda n: n.in_range(size), ns))

    @cache
    def peaks(field: Coordinate) -> set[Coordinate]:
        """returns the set of peaks reachable from this field"""
        if height(field) == 9:
            return {field}
        return set().union(
            *[
                peaks(neighbour)
                for neighbour in _neighbours(field)
                if height(neighbour) == height(field) + 1
            ]
        )

    @cache
    def trails(field: Coordinate) -> int:
        """returns the number of trails from this field"""
        if height(field) == 9:
            return 1
        return sum(
            [
                trails(neighbour)
                for neighbour in _neighbours(field)
                if height(neighbour) == height(field) + 1
            ]
        )

    return sum(
        [len(peaks(head)) if part == "a" else trails(head) for head in trailheads]
    )
