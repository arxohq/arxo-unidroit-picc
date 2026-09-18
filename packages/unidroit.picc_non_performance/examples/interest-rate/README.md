# Interest: the source names the rate, not the number

Two worked cases over the pinned canon of chapter 7 of the UNIDROIT Principles
(article 7.4.9). The norms stay in `unidroit.picc_non_performance`; here there
are only facts, questions and answers with their proof.

| Case | Question | Answer | Why |
|---|---|---|---|
| `RateAtPlaceOfPayment` | is there a right to interest | `COMPUTED` / `TRUE_ONLY` | article 7.4.9(1), whether or not the non-payment is excused |
| `RateAtPlaceOfPayment` | is it the bank rate at the place for payment | `COMPUTED` / `TRUE_ONLY` | first step of article 7.4.9(2): such a rate exists there |
| `RateAtPlaceOfPayment` | is it the rate in the State of the currency | `COMPUTED` / `NEITHER` | the second step did not fire — that is what a displaced step looks like |
| `RateAtPlaceOfPayment` | is it the rate fixed by law | `COMPUTED` / `NEITHER` | nor did the third |
| `NoRateAnywhere` | is there a right to interest | `COMPUTED` / `TRUE_ONLY` | unchanged: it never depended on the rate |
| `NoRateAnywhere` | is it the bank rate at the place for payment | `COMPUTED` / `NEITHER` | no such rate is presented |
| `NoRateAnywhere` | is it the rate fixed by law | `COMPUTED` / `TRUE_ONLY` | third step of article 7.4.9(2), reached only when the first two have nothing |

## Why this is the answer to article 78 of the Convention

Article 78 of the 1980 UN Convention gives the right to interest and stops
there: it names no rate, and practice has been filling that gap for decades.
Article 7.4.9(2) names a **rule of choice**, and the two cases show it working
from both ends — once when the ordinary rate exists, once when nothing is
available and the law of the currency's State decides.

What the model does not do is invent a percentage. Which rate applies is a legal
question and is answered; how much it is on a given day is a fact, and the case
brings it or nobody does.

## Absence is read as absence

The third step fires through `not_known`: the case simply does not assert that a
bank rate exists. That is different from asserting that no rate exists — the
canon asks for the first, and the model reads exactly that.

## Asking it yourself

From this directory, with the `law` binary on the path:

```sh
law ask . --case RateAtPlaceOfPayment --query-json queries/rate-at-place-of-payment.json
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
