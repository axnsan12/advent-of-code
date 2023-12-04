import functools
import shutil
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

import git
import termcolor
from aocd.examples import Example, Page
from aocd.get import most_recent_year, current_day
from aocd.models import Puzzle
from aocd.utils import get_plugins
from markdownify import markdownify

SOLUTIONS_ROOT = Path(__file__).parent

magenta = functools.partial(termcolor.colored, color='magenta')
yellow = functools.partial(termcolor.colored, color='yellow')
cyan = functools.partial(termcolor.colored, color='cyan')


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
    print(f'Created {magenta(day_dir)}')
    return True


def print_answer(name: str, actual: str, expected: str, already_solved: bool = False):
    actual = actual or ""
    good = expected and actual.strip() == expected.strip()
    if good:
        if already_solved:
            icon = "👑"
        else:
            icon = "✅"
    else:
        if not actual:
            icon = "❗"
        else:
            icon = "⛔"

    if actual:
        msg = f"answer: {yellow(repr(actual))}"
        if not good:
            if expected:
                msg += f", expected {yellow(repr(expected))}"
            else:
                msg += " (wrong)"
        elif already_solved:
            msg += " (already solved)"
    else:
        msg = "answer was empty"
    print(f'  {icon}  {cyan(name)} {msg}')
    return good


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

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('day', type=int, nargs='?', default=default_day or current_day(),
                        help='day (1-25)')
    parser.add_argument('year', type=int, nargs='?', default=default_year or most_recent_year(),
                        help=f'year (2015-{most_recent_year()})')

    parser.add_argument('-s', '--submit', action='store_true', default=False,
                        help='check solver results for example inputs')
    parser.add_argument('-e', '--example', action='store_true', default=False,
                        help='submit answers, or check solver results if answer is already known')

    args = parser.parse_args()

    puz = Puzzle(year=args.year, day=args.day)
    initialize_day(puz)
    update_text(puz)
    status = puz.answered_a + puz.answered_b

    print(f'Year {magenta(puz.year)}, Day {magenta(puz.day)}, Parts done: {magenta(status)}/2')
    if not args.example and not args.submit:
        parser.error('nothing to do! (one of -e, -s is required)')

    ep, = get_plugins()
    solver = ep.load()

    examples_ok = True
    if args.example:
        print(f'Checking examples')
        example_idx = 0
        for e in puz.examples:
            e: Example
            answer_a, answer_b = solver(year=puz.year, day=puz.day, data=e.input_data)
            answers = [
                (answer_a, e.answer_a),
                (answer_b, e.answer_b),
            ]

            for actual, expected in answers:
                if not expected:
                    continue

                example_idx += 1
                if not print_answer(f'Example #{example_idx}', actual, expected):
                    examples_ok = False

    if not examples_ok:
        return 1

    if args.submit:
        print(f'Submitting answers')
        repo = git.Repo(SOLUTIONS_ROOT.parent)
        answer_a, answer_b = solver(year=puz.year, day=puz.day, data=puz.input_data)
        answers = [
            (answer_a, 'answer_a'),
            (answer_b, 'answer_b'),
        ]

        for idx, (actual, expected_attr) in enumerate(answers, start=1):
            expected = getattr(puz, expected_attr, None)

            if expected or not actual:
                print_answer(f'Part {idx}', actual, expected, already_solved=True)
                continue

            from aocd.post import submit
            submit(actual, day=puz.day, year=puz.year, reopen=False)

            expected = getattr(puz, expected_attr, None)
            print_answer(f'Part {idx}', actual, expected)
            if not expected:
                return 1

            time.sleep(1.5)
            update_text(puz)
            repo.git.add('-A')
            repo.git.commit('-m', f'Solved {puz.year}/{puz.day:02} part {idx}')


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
    sys.exit(main() or 0)
