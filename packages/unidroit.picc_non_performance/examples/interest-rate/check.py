#!/usr/bin/env python3
"""Two worked cases on the rate of interest: the source names the rate, not the
number.

The expectations come FROM THE TEXT of the canon, not from the answers of the
engine:

  · article 7.4.9(1) — the aggrieved party is entitled to interest whether or not
    the non-payment is excused, and that answer does not depend on which rate
    applies;
  · article 7.4.9(2) — the rate is named in three steps: the average bank
    short-term lending rate at the place for payment, failing that the same rate
    in the State of the currency of payment, failing both the rate fixed by the
    law of that State. The three steps are three rules that displace one another
    through `not_known`, not one rule with provisos;
  · the value of the rate stays a fact of the case. The model answers WHICH rate
    applies and invents no percentage.

Article 78 of the 1980 Convention gives the right to interest and names no rate
at all — this is precisely the gap that article 7(2) of the Convention lets the
Principles fill.

Run from a checkout (Python >= 3.12) with the dependencies materialised first:

    python3 packs/examples/cases/materialize_deps.py \\
        corpus/laws/org/unidroit/picc-non-performance/examples/interest-rate
    python3 corpus/laws/org/unidroit/picc-non-performance/examples/interest-rate/check.py
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
    "RateAtPlaceOfPayment": {
        "entitled-to-interest": ("COMPUTED", "TRUE_ONLY"),
        "rate-at-place-of-payment": ("COMPUTED", "TRUE_ONLY"),
        "rate-in-state-of-currency": ("COMPUTED", "NEITHER"),
        "rate-fixed-by-law": ("COMPUTED", "NEITHER"),
    },
    "NoRateAnywhere": {
        "no-rate-entitled-to-interest": ("COMPUTED", "TRUE_ONLY"),
        "no-rate-at-place-of-payment": ("COMPUTED", "NEITHER"),
        "no-rate-fixed-by-law": ("COMPUTED", "TRUE_ONLY"),
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
            with tempfile.TemporaryDirectory(prefix="picc-interest-rate-") as temporary:
                questions = check(args.law, Path(temporary))
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"Interest rate: {len(EXPECTED)} cases, {questions} questions — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
