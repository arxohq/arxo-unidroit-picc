# arxo-unidroit-picc

Pinned canon, executable as it stands: source text with provenance, the
model built over it and the scenarios that check its answers. The norms
here are data — they are executed by `law`; this repository carries no
rule code of its own.

## Contents

| Package | Version | Scenarios | Dependencies |
|---|---|---|---|
| `unidroit.picc` | 0.1.0 | 5 | 0 |
| `unidroit.picc_formation` | 0.1.0 | 4 | 1 |
| `unidroit.picc_limitation` | 0.1.0 | 3 | 1 |
| `unidroit.picc_non_performance` | 0.1.0 | 4 | 1 |
| `unidroit.picc_obligations` | 0.1.0 | 4 | 1 |
| `unidroit.picc_performance` | 0.1.0 | 4 | 1 |
| `unidroit.picc_validity` | 0.1.0 | 4 | 1 |

## How it is verified

Every package is built by `package.py` with the pinned toolchain: compilation,
§267 scenarios on both evaluators, replay of saved evaluations and a rebuild
from the release itself. A failure of any step stops the build.

```sh
python3 tools/toolchain.py download --lock toolchain.lock.json --out /tmp/law-tools
python3 /tmp/law-tools/package.py packages/<name> \
    --lawc /tmp/law-tools/law-cli --offline --out /tmp/<name>-release
```

## Dependencies

Dependency bytes are pinned under `packages/<name>/deps/` and verified against the `contentHash` recorded in `law.lock`: the build and the CI are offline.

## Asking these packages

Two ways, the same slice of the canon and the same engine; the
difference is whose machine evaluates.

- **Hosted**: `https://mcp.arxo.io/mcp/picc` — requests are evaluated on Arxo infrastructure.
- **Local**: `docker compose -f mcp/compose.yml up` — nothing leaves the machine.

`mcp/pin.json` records what either one must answer from: the
content hash of the canon profile, the pinned packages, the ABI
version of the engine and the availability of the hosted endpoint.
An answer that cannot be traced to that pin is not this repository's
answer.

## Worked cases

Each collection is a case package of its own: the facts, the questions and
the answers, with the pinned canon as its dependency. Ask one from its
directory with `law ask .` — nothing is downloaded.

| Collection | Cases | Questions |
|---|---:|---:|
| [`packages/unidroit.picc/examples/applying-the-principles`](packages/unidroit.picc/examples/applying-the-principles/README.md) | 2 | 7 |
| [`packages/unidroit.picc_formation/examples/battle-of-forms`](packages/unidroit.picc_formation/examples/battle-of-forms/README.md) | 2 | 6 |
| [`packages/unidroit.picc_limitation/examples/limitation-periods`](packages/unidroit.picc_limitation/examples/limitation-periods/README.md) | 2 | 7 |
| [`packages/unidroit.picc_non_performance/examples/interest-rate`](packages/unidroit.picc_non_performance/examples/interest-rate/README.md) | 2 | 7 |
| [`packages/unidroit.picc_performance/examples/hardship`](packages/unidroit.picc_performance/examples/hardship/README.md) | 2 | 9 |

## Rights

Code and model: see `LICENSE`. The pinned texts of the publishers keep their
own terms of reproduction, listed per package in `NOTICE`; those terms are
not covered by the code licence.

Maintainer: Rifat Dzhumagulov (hi@arxo.io). Address: https://github.com/arxohq/arxo-unidroit-picc.
