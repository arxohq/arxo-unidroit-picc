#!/usr/bin/env python3
"""Two worked cases on hardship: the same events, one fact apart.

The expectations come FROM THE TEXT of the canon, not from the answers of the
engine:

  · article 6.2.1 — the party is bound to perform even though performance has
    become more onerous, and that answer does not depend on hardship at all;
  · article 6.2.2 — hardship needs four conditions, two of which are evaluative
    and answered by the organ (the §47.3 channel); the fourth, (d), is negative:
    an assumed risk excludes hardship;
  · article 6.2.3 — the request for renegotiation does not entitle the party to
    withhold performance, and only the failure to agree opens the way to the
    court;
  · article 6.2.3(4) — the court's power is a §127 power: the adaptation follows
    from its exercise together with the organ's answer on reasonableness.

Case 2 answers NEITHER rather than FALSE where hardship is excluded: the model
states no positive conclusion that there is no hardship, and says so honestly.

Run from a checkout (Python >= 3.12) with the dependencies materialised first:

    python3 packs/examples/cases/materialize_deps.py \\
        corpus/laws/org/unidroit/picc-performance/examples/hardship
    python3 corpus/laws/org/unidroit/picc-performance/examples/hardship/check.py
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
    "HardshipAndAdaptation": {
        "bound-to-perform-nevertheless": ("COMPUTED", "TRUE_ONLY"),
        "hardship-exists": ("COMPUTED", "TRUE_ONLY"),
        "entitled-to-request-renegotiation": ("COMPUTED", "TRUE_ONLY"),
        "request-does-not-entitle-to-withhold": ("COMPUTED", "TRUE_ONLY"),
        "may-resort-to-court": ("COMPUTED", "TRUE_ONLY"),
        "contract-adapted-by-court": ("COMPUTED", "TRUE_ONLY"),
    },
    "RiskAssumed": {
        "risk-bound-to-perform": ("COMPUTED", "TRUE_ONLY"),
        "risk-hardship-exists": ("COMPUTED", "NEITHER"),
        "risk-entitled-to-request-renegotiation": ("COMPUTED", "NEITHER"),
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
            with tempfile.TemporaryDirectory(prefix="picc-hardship-") as temporary:
                questions = check(args.law, Path(temporary))
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"Hardship: {len(EXPECTED)} cases, {questions} questions — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
