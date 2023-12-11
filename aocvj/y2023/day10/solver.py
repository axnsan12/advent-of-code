PIPE_CHARS = '-|LJ7F'


def bfs(grid: list[list[str]], start: tuple[int, int]) -> int:
    """Breadth-first search"""
    queue = [start]
    visited = set()
    parent = {}

    distance_matrix = [[0] * len(grid[0]) for _ in range(len(grid))]
    max_dist = 0
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue

        visited.add(node)
        parent_x, parent_y = parent.get(node, node)
        parent_dist = distance_matrix[parent_x][parent_y]
        distance_matrix[node[0]][node[1]] = parent_dist + 1
        max_dist = max(max_dist, parent_dist + 1)

        c = grid[node[0]][node[1]]
        if c == '-':
            steps = ((0, 1), (0, -1))
        elif c == '|':
            steps = ((1, 0), (-1, 0))
        elif c == 'L':
            steps = ((-1, 0), (0, 1))
        elif c == 'J' or c == 'S':  # s hardcoded for input...
            steps = ((0, -1), (-1, 0))
        elif c == '7':
            steps = ((0, -1), (1, 0))
        elif c == 'F':
            steps = ((1, 0), (0, 1))
        elif c == 'S':
            steps = ((0, 1), (1, 0), (0, -1), (-1, 0))
        else:
            raise ValueError(f'unknown pipe char {c}')
        for dx, dy in steps:
            x, y = node[0] + dx, node[1] + dy
            if (x, y) not in visited and grid[x][y] in PIPE_CHARS:
                queue.append((x, y))
                parent[(x, y)] = node

    for row in range(len(distance_matrix)):
        for col in range(len(distance_matrix[0])):
            if distance_matrix[row][col] != 0:
                num_predecessors = 0
                num_successors = 0
                for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    x, y = row + dx, col + dy
                    if distance_matrix[x][y] == distance_matrix[row][col] - 1:
                        num_predecessors += 1
                    if distance_matrix[x][y] == distance_matrix[row][col] + 1:
                        num_successors += 1

                window = [''.join(g[col-1:col+2]) for g in grid[row-1:row+2]]
                distance_window = [d[col-1:col+2] for d in distance_matrix[row-1:row+2]]
                # if (num_predecessors != 1 or num_successors != 1) and grid[row][col] != 'S':
                #     print(f'broken loop:\n' + "\n".join(window) + "\n" + "\n".join(map(str, distance_window)))
                #     raise AssertionError(f'broken loop! {row} {col} @ {window} {distance_window}')

    return max_dist


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

    answer_a = bfs(grid, start) - 1
    assert answer_a >= 1, f'??? {answer_a=}'
    grid_str = '\n'.join(''.join(row) for row in grid)
    print(f'{grid_str}')
    return answer_a, None
