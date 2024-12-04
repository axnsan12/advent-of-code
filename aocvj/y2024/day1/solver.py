from collections import Counter


def solve(data: str) -> tuple[int | str, int | str | None]:
    left, right = zip(*(map(int, line.split()) for line in data.splitlines()))
    left = sorted(left)
    right = sorted(right)
    answer_a = sum(abs(x - y) for x, y in zip(left, right))

    right_counts = Counter(right)
    answer_b = sum(x * right_counts[x] for x in left)
    return answer_a, answer_b
