import itertools


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = [ln.strip() for ln in data.splitlines() if ln.strip()]
    instructions = lines[0]

    graph = {}
    for ln in lines[1:]:
        letters = ''.join(c for c in ln if c.isalpha())
        src, left, right = letters[:3], letters[3:6], letters[6:]
        graph[src] = {'L': left, 'R': right}

    node = 'AAA'
    answer_a = 0
    for step in itertools.cycle(instructions):
        answer_a += 1
        node = graph[node][step]
        if node == 'ZZZ':
            break

    return answer_a, None
