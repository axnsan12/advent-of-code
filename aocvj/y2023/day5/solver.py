from more_itertools import chunked


def map_value(x, dest_range_start, src_range_start, range_len):
    if x in range(src_range_start, src_range_start + range_len):
        return dest_range_start + (x - src_range_start)

    return x


def map_range(r, dest_range_start, src_range_start, range_len) -> tuple[tuple[int, int] | None, list[tuple[int, int]]]:
    """
    For the range r, return a tuple of (mapped_range, unmapped_ranges);
    mapped_range: the new range in the destination domain, or None if r has no overlap with the mapping range
    unmapped_ranges: a potentially empty list of the ranges in the source domain that were split off

    Ranges are represented by (start, len) tuples
    """
    (input_range_start, input_range_len) = r
    input_range_end = input_range_start + input_range_len  # exclusive end; range is [start, end)

    if input_range_start < src_range_start:
        # input range starts before mapped range

        if input_range_end <= src_range_start:
            # ... and ends before mapped range, no-op
            return None, [(input_range_start, input_range_len)]

        if input_range_end <= src_range_start + range_len:
            # ... and ends within mapped range; splits off head, maps tail
            mapped = (dest_range_start, input_range_end - src_range_start)
            return mapped, [(input_range_start, input_range_len - mapped[1])]

        # ... and ends after mapped range, so contains it fully; splits off head and tail, maps middle
        mapped = (dest_range_start, range_len)
        return mapped, [
            (input_range_start, src_range_start - input_range_start),
            (src_range_start + range_len, input_range_end - src_range_start - range_len),
        ]

    if input_range_start >= src_range_start + range_len:
        # input range starts after mapped range, no-op
        return None, [(input_range_start, input_range_len)]

    # input range starts within mapped range
    if input_range_end <= src_range_start + range_len:
        # ... and ends within mapped range, so is fully contained by it
        mapped = (dest_range_start + input_range_start - src_range_start, input_range_len)
        return mapped, []

    # ... and ends after mapped range; splits off tail, maps head
    mapped = (dest_range_start + input_range_start - src_range_start, src_range_start + range_len - input_range_start)
    return mapped, [(src_range_start + range_len, input_range_end - src_range_start - range_len)]


def test_map_range():
    # no-op before
    assert map_range((2, 5), 100, 10, 3) == (None, [(2, 5)])
    assert map_range((2, 5), 100, 7, 3) == (None, [(2, 5)])

    # splits off head, maps tail
    assert map_range((2, 5), 100, 2, 3) == ((100, 3), [(5, 2)])
    assert map_range((2, 5), 100, 4, 10) == ((100, 3), [(2, 2)])
    assert map_range((2, 5), 100, 4, 4) == ((100, 3), [(2, 2)])
    assert map_range((2, 5), 100, 4, 3) == ((100, 3), [(2, 2)])

    # splits off head and tail, maps middle
    assert map_range((2, 5), 100, 4, 2) == ((100, 2), [(2, 2), (6, 1)])

    # no-op after
    assert map_range((2, 5), 100, 0, 2) == (None, [(2, 5)])

    # fully contained
    assert map_range((2, 5), 100, 0, 10) == ((102, 5), [])
    assert map_range((2, 5), 100, 2, 10) == ((100, 5), [])

    # splits off tail, maps head
    assert map_range((2, 5), 100, 0, 5) == ((102, 3), [(5, 2)])
    assert map_range((2, 5), 100, 2, 3) == ((100, 3), [(5, 2)])


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    lines_iter = iter(lines)

    seeds = []
    mappings = []
    while (line := next(lines_iter, None)) is not None:
        if line.startswith('seeds:'):
            seeds = line.split(':', maxsplit=1)[1].strip()
            seeds = [int(x) for x in seeds.split()]
        elif ' map:' in line:
            map_type = line.split()[0]
            source, _, dest = map_type.split('-')
            mapping_ranges = []
            while line := next(lines_iter, ''):
                mapping_ranges.append(tuple(map(int, line.split())))

            mappings.append(((source, dest), mapping_ranges))
        elif not line:
            continue
        else:
            raise AssertionError(f'wtf is {line}')

    seed_ranges = set(map(tuple, chunked(seeds, 2)))

    # part 1
    for (_, mapping_ranges) in mappings:
        mapped_seeds = list(seeds)
        for range_args in mapping_ranges:
            for (idx, x) in enumerate(seeds):
                mapped_x = map_value(x, *range_args)
                if mapped_x != x:
                    mapped_seeds[idx] = mapped_x

        seeds = mapped_seeds

    answer_a = min(seeds)

    # part 2
    for (_, mapping_ranges) in mappings:
        mapped_seed_ranges = set()

        done = False
        while seed_ranges and not done:
            done = True
            remaining = set()

            for r in seed_ranges:
                for range_args in mapping_ranges:
                    mapped_r, unmapped_ranges = map_range(r, *range_args)
                    if mapped_r is not None:
                        remaining.update(unmapped_ranges)
                        mapped_seed_ranges.add(mapped_r)
                        done = False
                        break
                else:
                    remaining.add(r)

            seed_ranges = remaining

        seed_ranges.update(mapped_seed_ranges)

    answer_b = min(seed_ranges)[0]
    return answer_a, answer_b
