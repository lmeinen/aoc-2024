import argparse
import importlib.util
import pathlib
import sys
import time
from typing import Callable, Literal

from aocd import submit
from aocd.models import Puzzle
from rich import print
from rich.columns import Columns
from rich.text import Text

p = argparse.ArgumentParser()
p.add_argument(
    "--days", nargs="+", type=int, default=list(range(1, 26))  # one or more values
)  # 1‑25
p.add_argument("--years", nargs="+", type=int, default=[2024])


def run(years: list[int], days: list[int]):
    # go through the list of years:
    for year in years:
        for day in days:
            solve_puzzle(year, day)


def solve_puzzle(year, day):
    puzzle = Puzzle(year, day)
    solve = import_solution(year, day)
    if solve is not None and callable(solve):
        for part in ("a", "b"):
            # Check if examples pass
            for example in puzzle.examples:
                expected = example.answers[0 if part == "a" else 1]
                actual = str(solve(part, example.input_data))
                if expected is not None and actual != expected:
                    pretty_print(
                        year,
                        day,
                        part,
                        state="SAMPLE_FAILED",
                        attempt=actual,
                        sample=expected,
                    )
                    return

            # Solve puzzle
            input = puzzle.input_data
            start = time.time()
            answer = solve(part, input)
            end = time.time()

            if not puzzle.answered(part):
                submit(
                    answer=answer,
                    part=part,
                    day=day,
                    year=year,
                    quiet=True,
                    reopen=True,
                )

            accepted = puzzle.answered(part) and str(answer) == (
                puzzle.answer_a if part == "a" else puzzle.answer_b
            )
            pretty_print(
                year,
                day,
                part,
                state="SUCCESS" if accepted else "REJECTED",
                time=end - start,
                attempt=answer,
            )
    else:
        pretty_print(year, day, "a", state="MISSING")
        pretty_print(year, day, "b", state="MISSING")


def pretty_print(
    year: int,
    day: int,
    part: Literal["a", "b"],
    *,
    state: Literal["MISSING", "SAMPLE_FAILED", "REJECTED", "SUCCESS"],
    time: float = 0,
    attempt: str | int | None = None,
    sample: str = "",
):
    yeartxt = Text(str(year), style="white")
    daytxt = Text(str(day), style="white")
    daytxt.align("right", 2)
    parttxt = Text(f"part {part}", style="white")
    columns = [yeartxt, daytxt, parttxt]

    if state == "MISSING":
        columns.append(
            Text(
                "❌ Missing implementation",
                style="red",
            )
        )
    elif state == "SAMPLE_FAILED":
        columns.append(
            Text(
                f"❌ Example failed" + f" - Expected: {sample[0]}; Actual: {sample[1]}",
                style="red",
            )
        )
    elif state == "REJECTED":
        columns.append(
            Text(
                f"{time:6.4f}s",
                style="red" if time > 1 else "orange" if time > 0.5 else "green",
            )
        )
        columns.append(
            Text(
                f"❌ Answer: {attempt}",
                style="red",
            )
        )
    else:
        columns.append(
            Text(
                f"{time:6.4f}s",
                style="red" if time > 1 else "orange" if time > 0.5 else "green",
            )
        )
        columns.append(
            Text(
                f"✅ Answer: {attempt}",
                style="green",
            )
        )

    print(Columns(columns))


def import_solution(
    year: int, day: int
) -> Callable[[Literal["a", "b"], str], str | int] | None:

    path = pathlib.Path(f"{year}/day_{day}.py").resolve()

    if not path.is_file():
        print("file does not exist")
        return None

    module_name = f"{year}.day_{day}"
    if module_name in sys.modules:
        module = sys.modules[module_name]
    else:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            print("spec failed")
            return None

        module = importlib.util.module_from_spec(spec)
        module.__package__ = f"{year}"

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"module loading failed: {e}")
            return None

        # Register it so future calls hit the cache
        sys.modules[module_name] = module

    return getattr(module, "solve", None)


args = p.parse_args()
run(args.years, args.days)
