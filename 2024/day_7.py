import math
from typing import Literal


def solve(part: Literal["a", "b"], input: str) -> int:
    sum = 0
    for line in input.splitlines():
        total_str, numbers_str = line.split(":", 1)
        total = int(total_str)
        numbers = list(map(int, numbers_str.split()))
        sum += check(total, numbers, part == "b")
    return sum


def check(total: int, numbers: list[int], with_concat: bool) -> int:
    results: set[int] = {numbers[0]}
    for x in numbers[1:]:
        nxt = set()
        l_shift = 10 ** (int(math.log10(x)) + 1)
        for res in results:
            if (sum := x + res) <= total:
                # addition is an option
                nxt.add(sum)

            if (product := x * res) <= total:
                # multiplication is an option
                nxt.add(product)

            if with_concat and (concatenation := res * l_shift + x) <= total:
                # concatenation is an option
                nxt.add(concatenation)
        results = nxt
    return total if total in results else 0
