#!/usr/bin/env python3
"""Two worked cases on the entry point of the instrument: does it apply, and how
is a term read.

The expectations come FROM THE TEXT of the canon, not from the answers of the
engine:

  · the Preamble grades its own answer by verbs — the Principles SHALL be
    applied when the parties agreed that they govern the contract, and MAY be
    applied when the parties chose general principles or no law at all. Asking
    the first question of the second contract comes back NEITHER: the Preamble
    does not say that;
  · article 1.7 puts a duty of good faith on each party towards the other, and
    article 1.7(2) makes any purported exclusion of it ineffective. The duty is
    a §123 position the document carries, not a fact of the case, and the
    positions query shows it ACTIVE in both directions;
  · article 4.1 has two levels with a textual order between them: where the
    common intention is established, the reading by reasonable persons falls
    away. The document stays REQUIRES_JUDGMENT because the organ has not been
    asked the second question — an honest state, not a failure;
  · article 4.6 does not give a meaning but chooses between meanings: the
    reading against the party that supplied an unclear term is preferred.

Whether a term is unclear, and whether a party acted in good faith, are
evaluative: they go to the organ of article 1.11 through the §47.3 channel.

Run from a checkout (Python >= 3.12) with the dependencies materialised first:

    python3 packs/examples/cases/materialize_deps.py \\
        corpus/laws/org/unidroit/picc/examples/applying-the-principles
    python3 corpus/laws/org/unidroit/picc/examples/applying-the-principles/check.py
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
    "DoTheyApply": {
        "principles-govern": ("COMPUTED", "TRUE_ONLY"),
        "lex-principles-govern": ("COMPUTED", "NEITHER"),
        "lex-may-be-applied": ("COMPUTED", "TRUE_ONLY"),
        "exclusion-of-good-faith-ineffective": ("COMPUTED", "TRUE_ONLY"),
        "good-faith-position": ("REQUIRES_JUDGMENT", None),
    },
    "ReadingATerm": {
        "contract-interpreted-by": ("REQUIRES_JUDGMENT", "TRUE_ONLY"),
        "reading-preferred": ("COMPUTED", "TRUE_ONLY"),
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
            # У вопроса о позициях (§172 positions) `truthStatus` у результата
            # нет: статусы несут normativeStatusSupports, и ожидание — None.
            got = (answer["evaluationStatus"], answer.get("truthStatus"))
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
            with tempfile.TemporaryDirectory(prefix="picc-applying-") as temporary:
                questions = check(args.law, Path(temporary))
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"Applying the Principles: {len(EXPECTED)} cases, {questions} questions — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
