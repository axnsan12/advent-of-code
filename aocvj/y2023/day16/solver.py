def get_delta(direction) -> tuple[int, int]:
    if direction == 'R':
        dx, dy = 0, 1
    elif direction == 'L':
        dx, dy = 0, -1
    elif direction == 'U':
        dx, dy = -1, 0
    elif direction == 'D':
        dx, dy = 1, 0
    else:
        raise AssertionError(f'invalid direction {direction}')

    return dx, dy


def trace_beam(grid: list[str], starting_direction: str, starting_idx: int) -> int:
    light = [[0] * len(grid[0]) for _ in range(len(grid))]
    sources = []
    dx, dy = get_delta(starting_direction)
    if dx == 0:
        sources.append((starting_idx, -dy, starting_direction))
    elif dy == 0:
        sources.append((-dx, starting_idx, starting_direction))

    used_sources = set()
    while sources:
        src = sources.pop()
        row, col, direction = src
        if src in used_sources:
            continue
        used_sources.add(src)

        dx, dy = get_delta(direction)
        while True:
            row += dx
            col += dy
            if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
                break

            light[row][col] = 1
            if grid[row][col] == '.':
                continue
            elif grid[row][col] == '-':
                # horizontal splitter
                if direction in 'RL':
                    continue

                sources.append((row, col, 'R'))
                sources.append((row, col, 'L'))
            elif grid[row][col] == '|':
                # vertical splitter
                if direction in 'UD':
                    continue

                sources.append((row, col, 'U'))
                sources.append((row, col, 'D'))
            elif grid[row][col] == '/':
                # mirror
                if direction == 'R':
                    direction = 'U'
                elif direction == 'L':
                    direction = 'D'
                elif direction == 'U':
                    direction = 'R'
                elif direction == 'D':
                    direction = 'L'

                sources.append((row, col, direction))
            elif grid[row][col] == '\\':
                # mirror
                if direction == 'R':
                    direction = 'D'
                elif direction == 'L':
                    direction = 'U'
                elif direction == 'U':
                    direction = 'L'
                elif direction == 'D':
                    direction = 'R'

                sources.append((row, col, direction))
            else:
                raise ValueError(f'unknown grid tile {grid[row][col]}')

            break

    return sum(sum(row) for row in light)


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = [ln.strip() for ln in data.splitlines() if ln.strip()]
    answer_a = trace_beam(grid, 'R', 0)

    answer_b = 0
    for idx in range(len(grid)):
        answer_b = max(answer_b, trace_beam(grid, 'R', idx))
        answer_b = max(answer_b, trace_beam(grid, 'L', idx))
    for idx in range(len(grid[0])):
        answer_b = max(answer_b, trace_beam(grid, 'U', idx))
        answer_b = max(answer_b, trace_beam(grid, 'D', idx))

    return answer_a, answer_b
