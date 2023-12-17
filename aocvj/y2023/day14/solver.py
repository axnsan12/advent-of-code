import numpy as np

BALL = 2
WALL = 1
EMPTY = 0


def print_grid(grid: np.ndarray):
    print()
    for ln in grid:
        print(''.join('#' if c == WALL else 'O' if c == BALL else '.' for c in ln))

    print()


def ndarray_to_tuple(grid: np.ndarray) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(ln) for ln in grid)


def bubble_up(grid: np.ndarray) -> np.ndarray:
    free_space_idx = [0] * len(grid[0])

    grid_copy = np.copy(grid)
    grid_copy[grid == BALL] = EMPTY
    for row_idx, ln in enumerate(grid):
        for col_idx, c in enumerate(ln):
            if c == BALL:
                free_idx = free_space_idx[col_idx]
                grid_copy[free_idx][col_idx] = BALL
                free_space_idx[col_idx] = free_idx + 1
            elif c == WALL:
                free_space_idx[col_idx] = row_idx + 1

    return grid_copy


def do_full_cycle(grid: np.ndarray) -> np.ndarray:
    for _ in range(4):
        grid = bubble_up(grid)
        grid = np.rot90(grid, axes=(1, 0))  # clockwise rotation

    return grid


def compute_load(grid: np.ndarray) -> int:
    answer = 0
    for row_idx, ln in enumerate(grid):
        for col_idx, c in enumerate(ln):
            if c == BALL:
                answer += len(grid) - row_idx

    return answer


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = data.splitlines(keepends=False)

    grid_np = np.array([[BALL if c == 'O' else WALL if c == '#' else EMPTY for c in ln] for ln in grid])
    grid_a = bubble_up(grid_np)

    answer_a = compute_load(grid_a)
    grid_b = grid_np

    history = {ndarray_to_tuple(grid_b): 0}
    target_step = 1_000_000_000

    answer_b = None
    for i in range(1, target_step):
        grid_b = do_full_cycle(grid_b)

        key = ndarray_to_tuple(grid_b)
        loop_start = history.get(key)
        if loop_start is not None:
            final_idx = (target_step - i) % (i - loop_start) + loop_start

            history_inv = {v: k for k, v in history.items()}
            answer_b = compute_load(history_inv[final_idx])
            break

        history[key] = i

    assert answer_b is not None, f's-a pizdit'
    return answer_a, answer_b
