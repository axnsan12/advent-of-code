import shutil
from argparse import ArgumentParser
from pathlib import Path

from aocd.examples import Example, Page
from aocd.get import most_recent_year, current_day
from aocd.models import Puzzle
from aocd.utils import get_plugins
from markdownify import markdownify

SOLUTIONS_ROOT = Path(__file__).parent


def get_number_from_dir_name(path: Path):
    if path.is_dir():
        name = path.name
        if name.startswith('day'):
            name = name[3:]
        if name.startswith('y'):
            name = name[1:]

        try:
            return int(name)
        except ValueError:
            pass

    return None


def update_text(puz: Puzzle):
    day_dir = SOLUTIONS_ROOT / f'y{puz.year}' / f'day{puz.day}'
    with open(day_dir / 'puzzle.md', 'w', encoding='utf-8') as f:
        # noinspection PyProtectedMember
        puzzle_page = Page.from_raw(html=puz._get_prose())
        puzzle_text = markdownify(puzzle_page.a_raw)
        if puzzle_page.b_raw:
            puzzle_text += "\n\n" + markdownify(puzzle_page.b_raw)
        f.write(puzzle_text)


def initialize_day(puz: Puzzle):
    day_dir = SOLUTIONS_ROOT / f'y{puz.year}' / f'day{puz.day}'
    try:
        day_dir.mkdir(exist_ok=False, parents=True)
    except FileExistsError:
        return False

    with open(day_dir / 'input.txt', 'w', encoding='utf-8') as f:
        f.write(puz.input_data)

    with open(day_dir / 'example.txt', 'w', encoding='utf-8') as f:
        w = 80
        for i, example in enumerate(puz.examples, start=1):
            if i > 1:
                f.write("\n\n")
            f.write(f" Example data {i}/{len(puz.examples)} ".center(w, "-") + "\n")
            f.write(example.input_data + "\n")
            f.write("-" * w + "\n")
            f.write("answer_a: " + (example.answer_a or "-") + "\n")
            f.write("answer_b: " + (example.answer_b or "-") + "\n")
            if example.extra:
                f.write("extra:" + example.extra)
            f.write("-" * w)

    shutil.copyfile(SOLUTIONS_ROOT / 'solver_template.py', day_dir / 'solver.py')
    return True


def print_answer(name: str, actual: str, expected: str):
    actual = actual or ""
    good = expected and actual.strip() == expected.strip()
    icon = "✅" if good else "⛔"
    msg = f"answer: {actual!r}"
    if not good:
        if expected:
            msg += f", expected {expected!r}"
        else:
            msg += " (wrong)"
    print(f'  {icon}  {name} {msg}')


def main():
    cwd = Path('.').resolve()

    default_day, default_year = None, None
    if cwd.is_relative_to(SOLUTIONS_ROOT):
        n = get_number_from_dir_name(cwd)
        if n is not None:
            if n >= 2015:
                default_year = n
            elif 0 < n <= 25:
                default_year = get_number_from_dir_name(cwd.parent)
                default_day = n

    parser = ArgumentParser()
    parser.add_argument('day', type=int, nargs='?', default=default_day or current_day())
    parser.add_argument('year', type=int, nargs='?', default=default_year or most_recent_year())

    submit_group = parser.add_mutually_exclusive_group(required=True)
    submit_group.add_argument('-s', '--submit', action='store_true', default=False)
    submit_group.add_argument('-e', '--example', action='store_true', default=False)

    args = parser.parse_args()

    puz = Puzzle(year=args.year, day=args.day)
    initialize_day(puz)
    update_text(puz)

    ep, = get_plugins()
    solver = ep.load()
    if args.example:
        print(f'Running solver for examples')
        for (idx, e) in enumerate(puz.examples, start=1):
            e: Example
            if e.extra:
                print(f'!!! Example #{idx} has extra: {e.extra!r}')
            answer_a, answer_b = solver(year=puz.year, day=puz.day, data=e.input_data)
            answers = [
                (answer_a, e.answer_a),
                (answer_b, e.answer_b),
            ]

            for actual, expected in answers:
                if not expected:
                    continue

                print_answer(f'Example #{idx}', actual, expected)

    if args.submit:
        print(f'Running solver and submitting answers')
        answer_a, answer_b = solver(year=puz.year, day=puz.day, data=puz.input_data)
        answers = [
            (answer_a, 'answer_a'),
            (answer_b, 'answer_b'),
        ]

        for idx, (actual, expected_attr) in enumerate(answers, start=1):
            expected = getattr(puz, expected_attr, None)
            if expected:
                if actual:
                    print_answer(f'Part {idx}', actual, expected)
                else:
                    print(f'  ℹ️  Part {idx} answer: {expected!r} (already solved)')

                continue

            if not actual:
                print(f'  ❗  Part {idx} answer was empty')
                continue

            from aocd.post import submit
            submit(actual, day=puz.day, year=puz.year, reopen=False)

            expected = getattr(puz, expected_attr, None)
            print_answer(f'Part {idx}', actual, expected)
            if not expected:
                break


def aocd_plugin(year, day, data):
    import importlib
    solver = importlib.import_module(f'aocvj.y{year}.day{day}.solver')
    a, b = solver.solve(data)
    if a is not None:
        a = str(a)
    if b is not None:
        b = str(b)
    return a, b


if __name__ == '__main__':
    main()
