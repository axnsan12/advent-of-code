def solve(data: str) -> tuple[int | str, int | str | None]:
    left, right = zip(*(map(int, line.split()) for line in data.splitlines()))
    left = sorted(left)
    right = sorted(right)
    answer_a = sum(abs(x - y) for x, y in zip(left, right))
    return answer_a, None
