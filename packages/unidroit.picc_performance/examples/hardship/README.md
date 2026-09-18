# Hardship: renegotiation and adaptation by the court

Two worked cases over the pinned canon of chapter 6 of the UNIDROIT Principles
(articles 6.2.1–6.2.3). The norms stay in `unidroit.picc_performance`; here
there are only facts, questions and answers with their proof.

The pair exists to show a boundary by an answer rather than by prose: the two
cases differ in **one fact** — whether the disadvantaged party had assumed the
risk of the events (article 6.2.2(d)) — and every conclusion that depends on
hardship falls away with it.

| Case | Question | Answer | Why |
|---|---|---|---|
| `HardshipAndAdaptation` | is the party still bound to perform | `COMPUTED` / `TRUE_ONLY` | article 6.2.1: the increased cost does not of itself excuse performance |
| `HardshipAndAdaptation` | is there hardship | `COMPUTED` / `TRUE_ONLY` | the four conditions of article 6.2.2 are met |
| `HardshipAndAdaptation` | may renegotiation be requested | `COMPUTED` / `TRUE_ONLY` | article 6.2.3(1), the request was made without undue delay |
| `HardshipAndAdaptation` | does the request suspend performance | `COMPUTED` / `TRUE_ONLY` | article 6.2.3(2) answers that it does **not** — a positive conclusion, not silence |
| `HardshipAndAdaptation` | may a party resort to the court | `COMPUTED` / `TRUE_ONLY` | article 6.2.3(3), no agreement within a reasonable time |
| `HardshipAndAdaptation` | is the contract adapted by the court | `COMPUTED` / `TRUE_ONLY` | article 6.2.3(4)(b), the §127 power exercised and found reasonable |
| `RiskAssumed` | is the party still bound to perform | `COMPUTED` / `TRUE_ONLY` | unchanged: article 6.2.1 never depended on hardship |
| `RiskAssumed` | is there hardship | `COMPUTED` / `NEITHER` | the assumed risk excludes it — and the model states no conclusion that hardship is absent |
| `RiskAssumed` | may renegotiation be requested | `COMPUTED` / `NEITHER` | it followed from hardship, and falls with it |

`NEITHER` is not `FALSE`. The canon gives no positive rule saying "there is no
hardship", so the honest answer is that nothing is established either way.

## The evaluative elements are answered by the organ

Two conditions of article 6.2.2 are not facts but assessments: whether the
equilibrium of the contract is **fundamentally** altered, and whether the events
could **reasonably** have been taken into account at the time of conclusion.
They are declared as §47.3 judgment channels with the organ of article 1.11
(court, including an arbitral tribunal), and the case supplies the organ's
answers as `origin adjudicated` — not as facts it invented.

The same holds for the reasonableness of termination or adaptation in article
6.2.3(4): without that answer the power exists but produces no effect.

## Running it

```sh
python3 packs/examples/cases/materialize_deps.py \
    corpus/laws/org/unidroit/picc-performance/examples/hardship
python3 corpus/laws/org/unidroit/picc-performance/examples/hardship/check.py
```

The checker asks all nine questions, compares each answer with the expectation
taken from the text, and then repeats every evaluation on the second
implementation and from the saved document — the three must agree byte for byte.

A single question, with its proof graph:

```sh
law ask corpus/laws/org/unidroit/picc-performance/examples/hardship \
    --case HardshipAndAdaptation --query-json queries/hardship-exists.json
```

## What this is not

A worked case is a model of an act applied to invented facts. It is neither
advice nor a precedent, and the answers of the organ are supplied by the case
rather than derived by the model.
