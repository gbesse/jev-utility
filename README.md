# jev-utility

**Turn calibrated probabilities and explicit mistake costs into thresholds, escalation bands, action rankings, and investment bounds.**

[![Tests](https://github.com/gbesse/jev-utility/actions/workflows/test.yml/badge.svg)](https://github.com/gbesse/jev-utility/actions/workflows/test.yml) ![MIT](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![Public alpha](https://img.shields.io/badge/status-public_alpha-orange)

## 30-second offline quick start

```sh
git clone https://github.com/gbesse/jev-utility.git && cd jev-utility
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt
python -m examples.offline_demo
```

The demo uses synthetic probabilities.

## Call real Jev

There is no network call: this package accepts probabilities from Jev or any other source. If Jev produced them, that upstream request is paid and goes to `api.typesafe.ai`; this toolkit never reads `TYPESAFE_API_KEY`. `python scripts/live_smoke.py` confirms the boundary.

## Library and integration

Use `optimal_threshold`, `abstention_band`, `expected_utility`, `calibration_report`, `fit_platt`, `fit_isotonic`, `calibration_split`, `value_of_information`, and `sensitivity`. The CLI reads JSONL `{probability,label}` rows and offers `threshold`, `calibrate`, `band`, `voi`, `sensitivity`, and `report --html` (multi-action problem tables currently use the Python API).

## How it decides

The binary cutoff is exactly `cost_fp/(cost_fp+cost_fn)`. Multi-action choices maximize the declared expected utility and report the margin. Human escalation wins only where declared human cost and residual error beat both automatic actions. A threshold is described as “optimal under stated costs, assuming calibration” unless an attached calibration report passes the configured ECE tolerance. See [the derivation](docs/method.md).

## Boundaries

Utilities are user assumptions, not facts. ECE depends on binning, holdouts can be noisy, and isotonic calibration can overfit small samples. Sensitivity uses declared factor scenarios rather than continuous symbolic bounds. No performance or live-model benchmark is claimed.

## Validation

Run `python -m compileall -q src tests`, `python -m unittest discover -s tests`, and `python -m examples.offline_demo`. CI runs them on Python 3.11 and 3.13.

## Related projects

[DecisionPacks](https://github.com/gbesse/decisionpacks), [Autonomy Meter](https://github.com/gbesse/autonomy-meter), and [jev-screen](https://github.com/gbesse/jev-screen) can consume cost-aware gates and escalation bands.

Independent project; not affiliated with TypeSafe AI. [API documentation](https://docs.typesafe.ai/api) · [Jev 1.13 model notes](https://docs.typesafe.ai/model-jaggedness/jev-1.13/)
