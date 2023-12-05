def map_value(x, dest_range_start, src_range_start, range_len):
    if x in range(src_range_start, src_range_start + range_len):
        return dest_range_start + (x - src_range_start)

    return x


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    lines_iter = iter(lines)

    seeds = []
    while (line := next(lines_iter, None)) is not None:
        if line.startswith('seeds:'):
            seeds = line.split(':', maxsplit=1)[1].strip()
            seeds = [int(x) for x in seeds.split()]
        elif ' map:' in line:
            map_type = line.split()[0]
            source, _, dest = map_type.split('-')
            mapped_seeds = list(seeds)
            while line := next(lines_iter, ''):
                range_args = list(map(int, line.split()))
                for (idx, x) in enumerate(seeds):
                    mapped_x = map_value(x, *range_args)
                    if mapped_x != x:
                        mapped_seeds[idx] = mapped_x

            seeds = mapped_seeds
        elif not line:
            continue
        else:
            raise AssertionError(f'wtf is {line}')

    answer_a = min(seeds)
    return answer_a, None
