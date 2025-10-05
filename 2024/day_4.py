from typing import List, Literal, Tuple


def solve(part: Literal["a", "b"], input: str) -> int:
    if part == "a":
        padding = 3
        anchor = "X"
        # possible word orderings
        bits = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        # interpret bits to construct character offsets in chars matrix
        offsets = [[(bx * o, by * o) for o in range(0, 4)] for (bx, by) in bits]
        key = "XMAS"
    else:
        padding = 1
        anchor = "A"
        # possible word orderings
        bits = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        # interpret bits to construct character offsets in chars matrix
        offsets = [
            [(-1 * bx, -1 * bx), (0, 0), (bx, bx), (-1 * by, by), (0, 0), (by, -1 * by)]
            for (bx, by) in bits
        ]
        key = "MASMAS"

    lines = input.splitlines()
    pad_line = lambda line: "." * padding + line + "." * padding
    chars = (
        ["." * len(pad_line(lines[0]))] * padding
        + [pad_line(l) for l in lines]
        + ["." * len(pad_line(lines[0]))] * padding
    )
    indices = [
        (i, j)
        for i in range(0, len(chars))
        for j in range(0, len(chars[0]))
        if chars[i][j] == anchor
    ]
    words = [_word(chars, idx, o) for idx in indices for o in offsets]
    return words.count(key)


def _word(
    chars: List[str], idx: Tuple[int, int], offsets: List[Tuple[int, int]]
) -> str:
    i, j = idx
    return "".join([chars[i + x][j + y] for (x, y) in offsets])
