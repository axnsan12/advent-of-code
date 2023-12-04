import regex


def solve(data: str) -> tuple[int | str, int | str | None]:
    digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    digits_by_name = {n: i for i, n in enumerate(digit_names, start=1)}
    digits_all = list(digit_names) + list(map(str, digits_by_name.values()))

    total_a = 0
    total_b = 0
    for line in data.splitlines(keepends=False):
        matches = regex.findall('|'.join(digits_all), line, overlapped=True)
        first = str(digits_by_name.get(matches[0], matches[0]))
        last = str(digits_by_name.get(matches[-1], matches[-1]))
        total_b += int(first + last)

        digits = [c for c in line if c.isdigit()]
        if digits:
            total_a += int(digits[0] + digits[-1])

    return total_a, total_b
