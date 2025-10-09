from typing import Sequence


def search(lst: Sequence[int], val: int) -> int:
    """returns insertion index for val in non-empty sorted list"""
    l = 0
    r = len(lst)
    while l < r:
        m = l + (r - l) // 2
        if lst[m] < val:
            l = m + 1
        elif lst[m] > val:
            r = m
        else:
            return m
    assert l <= r
    return l
