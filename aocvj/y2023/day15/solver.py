from collections import defaultdict


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

    boxes = defaultdict(dict)
    for step in data.strip().split(','):
        answer_a += compute_hash(step)

        if step.endswith('-'):
            step = step[:-1]
            boxes[compute_hash(step)].pop(step, None)
        else:
            step, val = step.split('=')
            boxes[compute_hash(step)][step] = int(val)

    answer_b = 0
    for box, lenses in sorted(boxes.items()):
        for j, (lens, val) in enumerate(lenses.items(), start=1):
            answer_b += (box + 1) * j * val

    return answer_a, answer_b
