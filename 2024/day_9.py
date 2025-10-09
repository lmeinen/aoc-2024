from __future__ import annotations

import itertools
import re
from collections import defaultdict, deque
from itertools import permutations
from typing import Literal

from util.algs import search
from util.coordinate import Coordinate


def solve(part: Literal["a", "b"], input: str) -> int:
    disk_map = list(map(int, input))
    if len(disk_map) % 2 == 0:
        disk_map.pop()  # we don't need free space at end of disk

    return solve_a(disk_map) if part == "a" else solve_b(disk_map)


def solve_a(disk_map: list[int]) -> int:
    checksum = 0

    position = 0
    L = 0
    L_block_id = 0
    R = len(disk_map) - 1
    R_block_id = len(disk_map) // 2
    while L <= R:
        if L % 2 == 0:
            # points at file: use present block
            checksum += L_block_id * position
        else:
            # points at free space: take block from R
            checksum += R_block_id * position
            disk_map[R] -= 1

        position += 1
        disk_map[L] -= 1

        # move pointers
        while disk_map[L] == 0 and L <= R:
            L += 1
            if L % 2 == 0:
                L_block_id += 1

        while disk_map[R] == 0 and L <= R:
            R -= 2
            R_block_id -= 1

    return checksum


def solve_b(disk_map: list[int]) -> int:
    files = []
    free = defaultdict(deque)
    position = 0
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            files.append((i // 2, position, size))
        elif size > 0:
            free[size].append(position)
        position += size

    checksum = 0
    for id, start, size in reversed(files):
        available_space = [
            (free[space][0], space)
            for space in range(size, 10)
            if len(free[space]) > 0 and free[space][0] < start
        ]

        if len(available_space) > 0:
            start, space = min(
                available_space,
                key=lambda t: t[0],
            )
            free[space].popleft()
            if (leftover := space - size) > 0:
                leftover_start = start + size
                free[leftover].insert(
                    search(free[leftover], leftover_start), leftover_start
                )
        checksum += id * (size * start + consecutive_sum(size - 1))

    return checksum


def consecutive_sum(n: int) -> int:
    return n * (n + 1) // 2
