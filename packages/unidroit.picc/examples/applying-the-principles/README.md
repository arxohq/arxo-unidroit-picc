# Do these Principles apply, and how is a term read

Two worked cases over the pinned canon of the Preamble and chapters 1 and 4 of
the UNIDROIT Principles. The norms stay in `unidroit.picc`; here there are only
facts, questions and answers with their proof.

This is the entry point of the instrument: before any rule of contract law
matters, the Preamble decides whether the Principles speak at all.

| Case | Question | Answer | Why |
|---|---|---|---|
| `DoTheyApply` | do the Principles govern the contract the parties chose them for | `COMPUTED` / `TRUE_ONLY` | Preamble: "They **shall** be applied when the parties have agreed…" |
| `DoTheyApply` | do they govern the contract that merely chose general principles | `COMPUTED` / `NEITHER` | the Preamble does not say that — a different verb, a different head |
| `DoTheyApply` | may they be applied to that second contract | `COMPUTED` / `TRUE_ONLY` | Preamble: "They **may** be applied when the parties have agreed… general principles of law, the lex mercatoria or the like" |
| `DoTheyApply` | is the purported exclusion of good faith effective | `COMPUTED` / `TRUE_ONLY` (ineffective) | article 1.7(2) |
| `DoTheyApply` | what positions does the document carry | `REQUIRES_JUDGMENT`, two `GoodFaith` duties `ACTIVE` | article 1.7(1): each party owes the other, and whether it was observed is for the organ |
| `ReadingATerm` | by which reading is the contract interpreted | `REQUIRES_JUDGMENT` / `TRUE_ONLY` | article 4.1(1): the common intention is established; the second level stays open until the organ is asked |
| `ReadingATerm` | which reading of the unclear clause is preferred | `COMPUTED` / `TRUE_ONLY` | article 4.6, contra proferentem |

## Two verbs, two heads

The Preamble is not a decorative opening. "Shall be applied" and "may be
applied" describe different legal situations, and the model keeps them apart:
a contract the Principles govern answers one question, a contract they may be
applied to answers another. Asking the wrong one returns `NEITHER` — the canon
states nothing about that combination, and the document says so rather than
guessing.

## A duty is not a fact

The duty of good faith is a §123 position: the document carries it, with a
bearer, a beneficiary and a maintenance goal. The positions query returns both
duties `ACTIVE` — one in each direction — while the evaluation as a whole stays
`REQUIRES_JUDGMENT`, because whether a party acted in good faith is a question
for the organ of article 1.11 and nobody has asked it yet.

An attempt to contract out of that duty is answered by article 1.7(2) with a
positive conclusion: the exclusion is ineffective. That is a rule of the
instrument, not a silence.

## Asking it yourself

From this directory, with the `law` binary on the path:

```sh
law ask . --case DoTheyApply --query-json queries/principles-govern.json
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
