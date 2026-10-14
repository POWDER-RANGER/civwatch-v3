"""Clearly marked synthetic samples for local UI development only."""
from datetime import datetime, timezone


def generate_simulated_obs(domain: str) -> dict:
    return {
        "source": "synthetic_generator",
        "measurement_class": "synthetic",
        "synthetic": True,
        "observed": False,
        "domain": domain,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "score": None,
        "flags": [],
        "confidence": None,
        "message": "Demo sample only; not a field measurement or detection.",
    }
