from __future__ import annotations

import itertools
import re
from collections import defaultdict
from itertools import permutations
from typing import Literal

from util.models import Coordinate


def solve(part: Literal["a", "b"], input: str) -> int:
    antennas: dict[str, list[Coordinate]] = defaultdict(list)
    lines = input.splitlines()
    for row, line in enumerate(lines):
        for match in re.finditer(r"[a-zA-Z0-9]", line):
            antennas[match.group()].append(Coordinate(row, match.start()))

    antinodes: set[Coordinate] = set()
    grid_size = (len(lines), len(lines[0]))

    def in_range(antinode: Coordinate) -> bool:
        return 0 <= antinode.x < grid_size[0] and 0 <= antinode.y < grid_size[1]

    for _, antenna_list in antennas.items():
        for a, b in permutations(antenna_list, 2):
            if part == "a":
                antinode = a + (a - b)  # reflects b across a
                if in_range(antinode):
                    antinodes.add(antinode)
            else:
                step = (b - a).normalize()
                antinodes |= set(
                    itertools.takewhile(
                        in_range, (b + step * i for i in itertools.count(0))
                    )
                )
                antinodes |= set(
                    itertools.takewhile(
                        in_range, (a - step * i for i in itertools.count(0))
                    )
                )

    return len(antinodes)
