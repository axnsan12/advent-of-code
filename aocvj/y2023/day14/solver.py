def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = data.splitlines(keepends=False)
    free_space_idx = [0] * len(grid[0])

    answer_a = 0
    for row_idx, ln in enumerate(grid):
        for col_idx, c in enumerate(ln):
            if c == 'O':
                answer_a += len(grid) - free_space_idx[col_idx]
                free_space_idx[col_idx] += 1
            elif c == '#':
                free_space_idx[col_idx] = row_idx + 1

    return answer_a, None
