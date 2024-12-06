from collections import defaultdict, deque


def topological_sort(precedence_pairs):
    # Create an adjacency list and in-degree dictionary
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)

    # Build the graph and calculate in-degrees
    for a, b in precedence_pairs:
        adj_list[b].append(a)
        in_degree[a] += 1
        if b not in in_degree:  # Ensure that nodes with no incoming edges have an in-degree of 0
            in_degree[b] = 0

    # Initialize a queue with nodes that have no dependencies (in-degree 0)
    queue = deque([node for node in in_degree if in_degree[node] == 0])

    topological_order = []

    while queue:
        node = queue.popleft()
        topological_order.append(node)

        # Decrease the in-degree of neighbors
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If we could not include all nodes, it means there was a cycle
    if len(topological_order) != len(in_degree):
        raise ValueError("Graph has a cycle, topological sort not possible.")

    return topological_order


def solve(data: str) -> tuple[int | str, int | str | None]:
    dependencies = defaultdict(list)  # key must come after values
    lines = iter(data.splitlines(keepends=False))
    for line in lines:
        if not line:
            break

        a, b = map(int, line.split('|'))
        dependencies[b].append(a)

    answer_a = 0
    for update in lines:
        pages = list(map(int, update.split(',')))
        pages_set = set(pages)

        applicable_rules = []
        for page in pages:
            for dep in dependencies[page]:
                if dep in pages_set:
                    applicable_rules.append((page, dep))

        topsort = topological_sort(applicable_rules)
        topsort_idx = {node: idx for idx, node in enumerate(topsort)}
        filtered_pages = [page for page in pages if page in topsort_idx]
        sorted_pages = sorted(filtered_pages, key=topsort_idx.get)
        if sorted_pages == filtered_pages:
            mid = len(pages) // 2
            answer_a += pages[mid]

    return answer_a, None
