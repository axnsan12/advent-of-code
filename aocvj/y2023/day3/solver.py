import re

import more_itertools


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = [f'.{ln}.' for ln in data.splitlines(keepends=False) if ln]
    empty = '.' * len(lines[0])
    lines = [empty, *lines, empty]

    answer_a = 0

    part_numbers = {}
    for window in more_itertools.windowed(enumerate(lines), 3):
        window: tuple[tuple[int, str], ...]
        for m in re.finditer(r'\d+', window[1][1]):
            part_number = int(m.group(0))
            is_part = False
            for (line_idx, ln) in window:
                for idx in range(m.start() - 1, m.end() + 1):
                    if ln[idx] != '.' and not ln[idx].isdigit():
                        is_part = True
                        part_id = (line_idx, idx)

                        check, numbers = part_numbers.setdefault(part_id, (ln[idx], []))
                        assert check == ln[idx]
                        numbers.append(part_number)
                        break

            if is_part:
                answer_a += int(m.group(0))

    answer_b = 0
    for (part_id, (part_char, part_numbers)) in part_numbers.items():
        if part_char == '*' and len(part_numbers) == 2:
            answer_b += part_numbers[0] * part_numbers[1]

    return answer_a, answer_b
