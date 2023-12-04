import re


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    for line in data.splitlines(keepends=False):
        m = re.match(r'Game (\d+): (.*)', line)
        game_id = int(m.group(1))
        rounds = m.group(2).split(';')

        max_red = 0
        max_green = 0
        max_blue = 0
        for r in rounds:
            cubes = r.split(',')
            for c in cubes:
                cnt, color = c.strip().split()
                cnt = int(cnt)
                if color == 'red':
                    max_red = max(max_red, cnt)
                elif color == 'green':
                    max_green = max(max_green, cnt)
                elif color == 'blue':
                    max_blue = max(max_blue, cnt)

        if max_red <= 12 and max_green <= 13 and max_blue <= 14:
            answer_a += game_id

    return answer_a, None
