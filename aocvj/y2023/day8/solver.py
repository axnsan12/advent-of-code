import itertools
import math
from typing import Callable


def solve_for_nodes(graph: dict[str, dict[str, str]], instructions: str,
                    nodes: list[str], goal_fn: Callable[[str], bool]) -> tuple[list[str], int]:
    count = 0
    for step in itertools.cycle(instructions):
        count += 1
        nodes = [graph[node][step] for node in nodes]
        if all(goal_fn(node) for node in nodes):
            break

    return nodes, count


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = [ln.strip() for ln in data.splitlines() if ln.strip()]
    instructions = lines[0]

    graph = {}
    for ln in lines[1:]:
        letters = ''.join(c for c in ln if c.isalnum())
        src, left, right = letters[:3], letters[3:6], letters[6:]
        graph[src] = {'L': left, 'R': right}

    if 'AAA' in graph:
        _, answer_a = solve_for_nodes(graph, instructions, ['AAA'], lambda n: n == 'ZZZ')
    else:
        answer_a = None

    start_nodes = [n for n in graph if n.endswith('A')]
    distances = set()
    for node in start_nodes:
        [goal], distance = solve_for_nodes(graph, instructions, [node], lambda n: n.endswith('Z'))
        _, check_distance = solve_for_nodes(graph, instructions, [goal], lambda n: n == goal)
        assert distance == check_distance, f'wtf??? {distance=} {check_distance=}'
        distances.add(distance)

    answer_b = math.lcm(*distances)
    return answer_a, answer_b
