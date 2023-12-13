import itertools

import numpy as np


def find_reflection(grid: np.ndarray, try_fix: int = None) -> int:
    for candidate_idx in range(1, len(grid)):
        i = candidate_idx - 1
        j = candidate_idx
        applied_fix = False

        while i >= 0 and j < len(grid):
            if not np.array_equal(grid[i], grid[j]):
                if try_fix is not None and not applied_fix:
                    # if there is one single difference, we can "fix" (ignore) it
                    if np.sum(grid[i] != grid[j]) == 1:
                        applied_fix = True
                        i -= 1
                        j += 1
                        continue

                break

            i -= 1
            j += 1
        else:
            if candidate_idx == try_fix:
                # we are trying to find an "imperfect" match (for part 2)
                # so skip the perfect match
                assert not applied_fix, f'wtf?? {try_fix} was supposed to be perfect!'
                continue

            return candidate_idx

    return 0


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = iter(data.splitlines(keepends=False))

    answer_a = 0
    answer_b = 0
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

        horizontal_fixed = find_reflection(grid, try_fix=horizontal)
        vertical_fixed = find_reflection(grid.T, try_fix=vertical)
        answer_b += horizontal_fixed * 100 + vertical_fixed

    return answer_a, answer_b
