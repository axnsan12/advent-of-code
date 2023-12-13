import itertools

import numpy as np


def find_reflection(grid: np.ndarray) -> int:
    for candidate_idx in range(1, len(grid)):
        i = candidate_idx - 1
        j = candidate_idx
        while i >= 0 and j < len(grid):
            if not np.array_equal(grid[i], grid[j]):
                break

            i -= 1
            j += 1
        else:
            return candidate_idx

    return 0


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = iter(data.splitlines(keepends=False))
    answer_a = 0
    while True:
        grid = []
        for ln in lines:
            ln = ln.strip()
            if not ln:
                break

            grid.append(np.array([c == '#' for c in ln], dtype=np.uint8))

        if not grid:
            break

        grid = np.array(grid)
        horizontal = find_reflection(grid)
        vertical = find_reflection(grid.T)
        answer_a += horizontal * 100 + vertical

    return answer_a, None
