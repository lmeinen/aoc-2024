import importlib.util
import pathlib
import time
from typing import Callable, Literal, Tuple

from aocd import submit
from aocd.models import Puzzle
from rich import print
from rich.columns import Columns
from rich.text import Text

# TODO: wrap in args
years = [2024]


def run():
    # go through the list of years:
    for year in years:
        for day in range(1, 26):
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
        return None

    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None:
        return None

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    except Exception as e:
        return None

    return getattr(module, "solve", None)


run()
