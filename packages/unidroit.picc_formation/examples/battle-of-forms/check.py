#!/usr/bin/env python3
"""Two worked cases on the battle of forms: a rule where the Convention is silent.

The expectations come FROM THE TEXT of the canon, not from the answers of the
engine:

  · article 2.1.22 — where both parties use standard terms, the contract is
    concluded on the agreed terms and on those standard terms that are common in
    substance; the terms that differ knock each other out, so the model says
    nothing about them and the answer is NEITHER rather than FALSE;
  · article 2.1.22, final words — a party that indicated in advance that it does
    not intend to be bound defeats the rule itself, and every conclusion drawn
    from it falls away;
  · article 2.1.20 — a term the other party could not reasonably have expected is
    ineffective whether or not the forms agree; whether it is surprising is
    evaluative and is answered by the organ (the §47.3 channel).

Article 19 of the 1980 Convention has no knock-out rule at all: on these same
facts it would need a choice between two readings of its silence.

Run from a checkout (Python >= 3.12) with the dependencies materialised first:

    python3 packs/examples/cases/materialize_deps.py \\
        corpus/laws/org/unidroit/picc-formation/examples/battle-of-forms
    python3 corpus/laws/org/unidroit/picc-formation/examples/battle-of-forms/check.py
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
    "KnockOut": {
        "contract-on-common-terms": ("COMPUTED", "TRUE_ONLY"),
        "arbitration-is-part": ("COMPUTED", "TRUE_ONLY"),
        "liability-cap-is-part": ("COMPUTED", "NEITHER"),
        "forum-clause-ineffective": ("COMPUTED", "TRUE_ONLY"),
    },
    "NotBoundInAdvance": {
        "refusal-contract-on-common-terms": ("COMPUTED", "NEITHER"),
        "refusal-arbitration-is-part": ("COMPUTED", "NEITHER"),
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
            with tempfile.TemporaryDirectory(prefix="picc-battle-of-forms-") as temporary:
                questions = check(args.law, Path(temporary))
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"Battle of forms: {len(EXPECTED)} cases, {questions} questions — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
