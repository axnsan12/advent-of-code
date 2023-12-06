import re


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    times = list(map(int, re.findall(r'(\d+)', lines[0])))
    distances = list(map(int, re.findall(r'(\d+)', lines[1])))

    answer_a = 1
    for (max_time, distance) in zip(times, distances):
        possible = 0
        for t in range(1, max_time):
            speed = t
            my_distance = speed * (max_time - t)
            if my_distance > distance:
                print(f'{t}/{max_time} {my_distance} > {distance}')
                possible += 1

        answer_a *= possible

    return answer_a, None
