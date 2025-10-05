import re
from typing import Literal


def solve(part: Literal["a", "b"], input: str) -> int:
    valid = input.replace("\n", "")
    if part == "b":
        invalid = [
            (m.start(), m.end())
            for m in re.finditer(r"(?:don't\(\)).*?(?:do\(\)|$)", valid)
        ]
        valid = "".join(
            [
                valid[start:end]
                for ((_, start), (end, _)) in zip(
                    [(0, 0)] + invalid, invalid + [(len(valid), len(valid))]
                )
            ]
        )
    return sum(
        [int(a) * int(b) for a, b in re.findall(r"(?:mul\((\d+),(\d+)\))", valid)]
    )
