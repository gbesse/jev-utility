"""Compare deterministic cutoffs under different declared mistake costs."""
import json

from jev_utility import optimal_threshold

PROBABILITIES = [0.15, 0.45, 0.75, 0.95]
SCENARIOS = {
    "balanced": (1, 1),
    "false_positive_costly": (4, 1),
    "false_negative_costly": (1, 4),
}


def example():
    return {
        "source": "synthetic probabilities and assumed costs; no model calls",
        "scenarios": {
            name: {
                "cost_false_positive": costs[0],
                "cost_false_negative": costs[1],
                "cutoff": optimal_threshold(*costs),
                "accepted_probabilities": [p for p in PROBABILITIES if p >= optimal_threshold(*costs)],
            }
            for name, costs in SCENARIOS.items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(example(), indent=2, sort_keys=True))
