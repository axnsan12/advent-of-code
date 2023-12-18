def trace_beam(grid: list[str]) -> int:
    light = [[0] * len(grid[0]) for _ in range(len(grid))]
    sources = [(0, -1, 'R')]

    used_sources = set()
    while sources:
        src = sources.pop()
        row, col, direction = src
        if src in used_sources:
            continue
        used_sources.add(src)

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
    answer_a = trace_beam(grid)
    return answer_a, None
