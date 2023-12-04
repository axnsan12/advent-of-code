import re

import more_itertools


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = [f'.{ln}.' for ln in data.splitlines(keepends=False) if ln]
    empty = '.' * len(lines[0])
    lines = [empty, *lines, empty]

    answer_a = 0

    for (before, line, after) in more_itertools.windowed(lines, 3):
        for m in re.finditer(r'\d+', line):
            is_part = False
            for ln in (before, line, after):
                for idx in range(m.start() - 1, m.end() + 1):
                    if ln[idx] != '.' and not ln[idx].isdigit():
                        is_part = True
                        break

            if is_part:
                answer_a += int(m.group(0))

    return answer_a, None
