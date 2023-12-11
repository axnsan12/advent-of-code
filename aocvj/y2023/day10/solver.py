import itertools

import matplotlib.path
import numpy as np

PIPE_CHARS = {
    '-': ((0, -1), (0, 1)),
    '|': ((-1, 0), (1, 0)),
    'L': ((-1, 0), (0, 1)),
    'J': ((-1, 0), (0, -1)),
    '7': ((0, -1), (1, 0)),
    'F': ((0, 1), (1, 0)),
}

ALL_DIRECTIONS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def detect_start_char_type(grid: list[list[str]], start: tuple[int, int]) -> str:
    row, col = start

    steps = []
    neighbors = ''
    for dx, dy in ALL_DIRECTIONS:
        x, y = row + dx, col + dy
        c = grid[x][y]
        neighbors += c
        if c in PIPE_CHARS and (-dx, -dy) in PIPE_CHARS[c]:
            steps.append((dx, dy))

    assert len(steps) == 2, f'??? {steps}'
    steps = tuple(sorted(steps))
    for candidate, candidate_steps in PIPE_CHARS.items():
        if steps == candidate_steps:
            return candidate

    raise AssertionError(f'failed to deduce start char type {steps} {neighbors}')


def trace_loop(grid: list[list[str]], start: tuple[int, int]) -> list[tuple[int, int]]:
    nodes = [start]
    next_node = start

    while True:
        c = grid[next_node[0]][next_node[1]]
        if c == 'S':
            c = detect_start_char_type(grid, next_node)
        if c == '-':
            steps = ((0, 1), (0, -1))
        elif c == '|':
            steps = ((1, 0), (-1, 0))
        elif c == 'L':
            steps = ((-1, 0), (0, 1))
        elif c == 'J':
            steps = ((0, -1), (-1, 0))
        elif c == '7':
            steps = ((0, -1), (1, 0))
        elif c == 'F':
            steps = ((1, 0), (0, 1))
        else:
            raise ValueError(f'unknown pipe char {c}')
        for dx, dy in steps:
            x, y = next_node[0] + dx, next_node[1] + dy
            if (x, y) != nodes[-1]:
                nodes.append(next_node)
                next_node = (x, y)
                break
        else:
            raise AssertionError(f'failed to find next node {next_node} {steps}')

        if next_node == start:
            break

    return nodes


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    lines = ['.' + ln.strip() + '.' for ln in lines if ln.strip()]
    lines = ['.' * len(lines[0])] + lines + ['.' * len(lines[0])]
    grid = [list(ln) for ln in lines]

    start = None
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'S':
                start = (i, j)
                break
    assert start is not None, f'failed to find start {grid}'

    loop_points = trace_loop(grid, start)
    answer_a = len(loop_points) // 2

    loop_points_set = set(loop_points)
    other_points = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) not in loop_points_set:
                other_points.append((row, col))

    poly = matplotlib.path.Path(np.array(loop_points))
    inside_points = [
        p
        for p, is_inside
        in zip(other_points, poly.contains_points(np.array(other_points)))
        if is_inside
    ]

    for r, c in inside_points:
        grid[r][c] = 'X'
    grid_str = '\n'.join(''.join(row) for row in grid)
    print(f'{grid_str}')
    answer_b = len(inside_points)
    assert answer_a >= 1, f'??? {answer_a=}'
    return answer_a, answer_b
