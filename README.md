# arxo-unidroit-picc

Pinned canon, executable as it stands: source text with provenance, the
model built over it and the scenarios that check its answers. The norms
here are data — they are executed by `law`; this repository carries no
rule code of its own.

## Contents

| Package | Version | Scenarios | Dependencies |
|---|---|---|---|
| `unidroit.picc` | 0.1.0 | 4 | 0 |
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

## Rights

Code and model: see `LICENSE`. The pinned texts of the publishers keep their
own terms of reproduction, listed per package in `NOTICE`; those terms are
not covered by the code licence.

Maintainer: Arxo Law (inji.qaz@gmail.com). Address: https://github.com/arxohq/arxo-unidroit-picc.
