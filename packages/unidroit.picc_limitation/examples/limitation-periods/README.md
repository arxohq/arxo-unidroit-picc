# Limitation: the day the count begins

Two worked cases over the pinned canon of chapter 10 of the UNIDROIT Principles
(articles 10.1–10.11). The norms stay in `unidroit.picc_limitation`; here there
are only facts, questions and answers with their proof.

| Case | Question | Answer | Why |
|---|---|---|---|
| `TwoPeriodsRunning` | is the exercise of the right limited at all | `COMPUTED` / `TRUE_ONLY` | article 10.1(1) |
| `TwoPeriodsRunning` | does the general period expire on **11 March 2023** | `COMPUTED` / `TRUE_ONLY` | three years from the day **after** 10 March 2020 (article 10.2(1)) |
| `TwoPeriodsRunning` | does it expire on 10 March 2023 | `COMPUTED` / `NEITHER` | no rule makes that day the last one |
| `TwoPeriodsRunning` | does the maximum period expire on 16 January 2029 | `COMPUTED` / `TRUE_ONLY` | ten years from the day after 15 January 2019 (article 10.2(2)) |
| `ExpiryNotInvoked` | is the right extinguished | `COMPUTED` / `TRUE_ONLY` (not extinguished) | article 10.9(1) |
| `ExpiryNotInvoked` | is its exercise barred | `COMPUTED` / `NEITHER` | article 10.9(2): the obligor never asserted the expiry |
| `ExpiryNotInvoked` | may a set-off still be exercised | `COMPUTED` / `TRUE_ONLY` | article 10.10, until the expiry is asserted |

## One day is an answer, not a footnote

Article 10.2 opens both periods with the same words: *beginning on the day after
the day…*. The §86 policy of the package is therefore `start_count next_day`,
and the case asks the wrong day on purpose — 10 March 2023 comes back `NEITHER`.
A reader who expected the 10th learns the difference from the model rather than
from a warning in prose.

## The policy belongs to the document that answers

The `deadline policy PICC_LIMITATION` is declared in **this** package, not only
in the one that owns the norms. A case is counted by the policy of the document
that answers it; without the declaration the evaluation refuses with
`LDC-E1332` instead of quietly counting by some default.

## Expiry does nothing until someone says so

The second case holds two answers that only look contradictory: the right is not
extinguished (article 10.9(1)) **and** its exercise is not barred (article
10.9(2)), because nobody raised the defence. Article 10.10 reads the same
silence from the other side: the set-off is still available.

`NEITHER` for "is the exercise barred" is again not `FALSE`. The canon states no
rule concluding that the exercise is free; it states that the bar needs an
assertion that has not happened.

## Asking it yourself

From this directory, with the `law` binary on the path:

```sh
law ask . --case TwoPeriodsRunning --query-json queries/general-period-expires-on-11-march.json
```

The answer comes back as an evaluation document: the result, the proof graph
that produced it, the pinned sources behind every rule and the hashes that make
the run repeatable. Every file listed in `queries/` is a question you can ask.

The dependencies of the collection travel with it, so nothing is downloaded.

Where these packages are maintained, `check.py` asks all of the questions above
in one go, compares each answer with the expectation taken from the text, and
then repeats every evaluation on a second implementation and from the saved
document — the three must agree byte for byte.

## What this is not

A worked case is a model of an act applied to invented facts. It is neither
advice nor a precedent.
