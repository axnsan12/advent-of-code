from collections import defaultdict


def flood_fill(grid, pos, c):
    queue = [pos]
    while queue:
        x, y = queue.pop()
        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
            continue
        if grid[x][y] != '.':
            continue
        grid[x][y] = c
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def solve(data: str) -> tuple[int | str, int | str | None]:
    total_dist = defaultdict(int)
    dig_plan = []
    for ln in data.splitlines():
        direction, dist, color = ln.split()
        dist = int(dist)
        total_dist[direction] += dist
        dig_plan.append((direction, dist, color))

    width = total_dist['L'] + total_dist['R'] + 5
    height = total_dist['U'] + total_dist['D'] + 5
    start = (total_dist['U'] + 1, total_dist['L'] + 1)

    grid = [['.' for _ in range(width)] for _ in range(height)]
    for (direction, dist, _) in dig_plan:
        if direction == 'R':
            for i in range(dist + 1):
                grid[start[0]][start[1] + i] = '#'
            start = (start[0], start[1] + dist)
        elif direction == 'L':
            for i in range(dist + 1):
                grid[start[0]][start[1] - i] = '#'
            start = (start[0], start[1] - dist)
        elif direction == 'U':
            for i in range(dist + 1):
                grid[start[0] - i][start[1]] = '#'
            start = (start[0] - dist, start[1])
        elif direction == 'D':
            for i in range(dist + 1):
                grid[start[0] + i][start[1]] = '#'
            start = (start[0] + dist, start[1])

    flood_fill(grid, (0, 0), '?')
    answer_a = width * height - sum(ln.count('?') for ln in grid)
    return answer_a, None
