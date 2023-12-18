def compute_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h


def solve(data: str) -> tuple[int | str, int | str | None]:
    compute_hash("HASH")

    answer_a = 0
    for step in data.strip().split(','):
        answer_a += compute_hash(step)
    return answer_a, None
