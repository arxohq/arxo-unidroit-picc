#!/usr/bin/env python3
"""Two worked cases on limitation: the day the count begins, and an expiry nobody
invoked.

The expectations come FROM THE TEXT of the canon, not from the answers of the
engine:

  · article 10.2 opens both periods with "beginning on the day after the day…",
    so the general period of three years from 10 March 2020 expires on 11 March
    2023 and the maximum period of ten years from 15 January 2019 expires on
    16 January 2029; the same question asked about 10 March 2023 comes back
    NEITHER, because no rule makes that day the last one;
  · article 10.9(1) — expiry does not extinguish the right;
  · article 10.9(2) — expiry has no effect until the obligor asserts it as a
    defence, so the exercise of the right is not barred while nobody has;
  · article 10.10 — the obligee may exercise a set-off until that assertion; the
    rule reads the obligor's silence as a fact of the case, not as its denial.

The §86 policy is declared by THIS package, not by the one that owns the norms:
a case is counted by the policy of the document that answers it (LDC-E1332).

Run from a checkout (Python >= 3.12) with the dependencies materialised first:

    python3 packs/examples/cases/materialize_deps.py \\
        corpus/laws/org/unidroit/picc-limitation/examples/limitation-periods
    python3 corpus/laws/org/unidroit/picc-limitation/examples/limitation-periods/check.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[6]
sys.path.insert(0, str(ROOT / "engines" / "lawref"))

from lawref.canon import canonical_bytes  # noqa: E402
from lawref.cases import check_registration  # noqa: E402
from lawref.evaluator import EvaluationRequest, evaluate  # noqa: E402

#: case → question → (evaluationStatus, truthStatus) FROM THE TEXT of the canon.
EXPECTED = {
    "TwoPeriodsRunning": {
        "limitation-governed": ("COMPUTED", "TRUE_ONLY"),
        "general-period-expires-on-11-march": ("COMPUTED", "TRUE_ONLY"),
        "general-period-expires-on-10-march": ("COMPUTED", "NEITHER"),
        "maximum-period-expires-on": ("COMPUTED", "TRUE_ONLY"),
    },
    "ExpiryNotInvoked": {
        "expiry-right-not-extinguished": ("COMPUTED", "TRUE_ONLY"),
        "expiry-exercise-barred": ("COMPUTED", "NEITHER"),
        "expiry-set-off-still-available": ("COMPUTED", "TRUE_ONLY"),
    },
}


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"{' '.join(command)}\n{completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


def check(law: str, output: Path) -> int:
    entries = check_registration(PACKAGE)
    if {entry.name for entry in entries} != set(EXPECTED):
        raise RuntimeError("the registered cases differ from the ones checked here")
    questions = 0
    for entry in entries:
        for query, expected in EXPECTED[entry.name].items():
            saved = output / entry.name / query
            result = run_json([
                law, "ask", str(PACKAGE), "--case", entry.name,
                "--query-json", str(PACKAGE / "queries" / f"{query}.json"),
                "--out", str(saved),
            ])
            answer, = result["results"]
            got = (answer["evaluationStatus"], answer["truthStatus"])
            if got != expected:
                raise RuntimeError(f"{entry.name}/{query}: expected {expected}, got {got}")
            request = json.loads((saved / "request.json").read_bytes())
            oracle = evaluate(EvaluationRequest.from_dict(request))
            replay = run_json([law, "eval", str(saved)])
            expected_bytes = canonical_bytes(result)
            if canonical_bytes(oracle) != expected_bytes:
                raise RuntimeError(f"{entry.name}/{query}: Rust != Python")
            if canonical_bytes(replay) != expected_bytes:
                raise RuntimeError(f"{entry.name}/{query}: ask != replay")
            questions += 1
        print(f"{entry.name}: {len(EXPECTED[entry.name])} question(s) — "
              "text expectations, Rust/Python and replay all agree", flush=True)
    return questions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law", default=str(ROOT / "law"),
                        help="the law binary, or the launcher of a checkout")
    parser.add_argument("--out", type=Path,
                        help="keep request/result; a temporary directory by default")
    args = parser.parse_args()
    try:
        if args.out:
            questions = check(args.law, args.out.resolve())
        else:
            with tempfile.TemporaryDirectory(prefix="picc-limitation-") as temporary:
                questions = check(args.law, Path(temporary))
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"Limitation periods: {len(EXPECTED)} cases, {questions} questions — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
