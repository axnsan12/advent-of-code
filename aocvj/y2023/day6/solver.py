import re
from tqdm import tqdm


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    times_str = re.findall(r'(\d+)', lines[0])
    distances_str = re.findall(r'(\d+)', lines[1])
    times = list(map(int, times_str))
    distances = list(map(int, distances_str))
    time_concat = int(''.join(times_str))
    distance_concat = int(''.join(distances_str))

    answer_a = 1
    for (max_time, distance) in zip(times, distances):
        possible = 0
        for t in range(1, max_time):
            speed = t
            my_distance = speed * (max_time - t)
            if my_distance > distance:
                possible += 1

        answer_a *= possible

    answer_b = 0
    for t in tqdm(range(1, time_concat)):
        speed = t
        my_distance = speed * (time_concat - t)
        if my_distance > distance_concat:
            answer_b += 1

    return answer_a, answer_b
