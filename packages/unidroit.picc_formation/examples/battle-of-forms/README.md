# The battle of forms: a rule where the Convention is silent

Two worked cases over the pinned canon of chapter 2 of the UNIDROIT Principles
(articles 2.1.19–2.1.22). The norms stay in `unidroit.picc_formation`; here
there are only facts, questions and answers with their proof.

| Case | Question | Answer | Why |
|---|---|---|---|
| `KnockOut` | is the contract on the common terms | `COMPUTED` / `TRUE_ONLY` | article 2.1.22: both parties used standard terms and agreed on everything else |
| `KnockOut` | is the arbitration clause part of it | `COMPUTED` / `TRUE_ONLY` | the two forms say the same thing in substance |
| `KnockOut` | is the liability cap part of it | `COMPUTED` / `NEITHER` | the caps differ, so they knock each other out — the model states nothing about them |
| `KnockOut` | is the buried forum clause effective | `COMPUTED` / `TRUE_ONLY` (ineffective) | article 2.1.20: the organ found it one the other party could not reasonably have expected |
| `NotBoundInAdvance` | is the contract on the common terms | `COMPUTED` / `NEITHER` | the closing words of article 2.1.22: a party indicated in advance it would not be bound |
| `NotBoundInAdvance` | is the arbitration clause part of it | `COMPUTED` / `NEITHER` | it followed from the knock-out conclusion, and falls with it |

## Why this case exists

Article 2.1.22 states the knock-out **as a rule**. Article 19 of the 1980 UN
Convention has no such rule at all, and its silence is read in two ways — those
two readings are declared in `intl.uncitral.cisg_formation` and a case there has
to choose between them. On the same facts the Principles answer from the text.

The difference is visible in the answers, not in the commentary: here the
question is `COMPUTED`, there it depends on a reading the case must select.

## Knock-out means silence, not denial

`NEITHER` for the liability cap is the whole point. The canon does not say "the
differing term is excluded"; it says the contract is concluded on the terms that
are common in substance. What happens to the rest is simply not stated, and the
model does not invent a conclusion to fill the gap.

The same shape appears in case 2 from a different cause: there the rule itself is
defeated, so nothing downstream is established either.

## Asking it yourself

From this directory, with the `law` binary on the path:

```sh
law ask . --case KnockOut --query-json queries/contract-on-common-terms.json
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
advice nor a precedent, and the answers of the organ are supplied by the case
rather than derived by the model.
