"""Normalize device-reported and synthetic observations into one bounded schema."""
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class NormalizedObservation(BaseModel):
    model_config = ConfigDict(extra="allow")
    sensor_id: str
    timestamp: str
    domain: str
    payload: dict[str, Any] = Field(default_factory=dict)
    score: float | None = None
    flags: list[str] = Field(default_factory=list)
    confidence: float | None = None
    observation_mode: str = "unknown"
    synthetic: bool = False


def normalize_observation(raw: dict[str, Any], domain: str, sensor_id: str) -> NormalizedObservation:
    """Keep source mode explicit; do not infer threat state from missing metrics."""
    return NormalizedObservation(
        sensor_id=str(raw.get("sensor_id") or sensor_id)[:128],
        timestamp=str(raw.get("timestamp") or ""),
        domain=domain,
        payload=raw.get("payload") if isinstance(raw.get("payload"), dict) else {},
        score=raw.get("score") if isinstance(raw.get("score"), (int, float)) else None,
        flags=[str(x)[:160] for x in raw.get("flags", []) if isinstance(x, str)][:20],
        confidence=raw.get("confidence") if isinstance(raw.get("confidence"), (int, float)) else None,
        observation_mode=str(raw.get("observation_mode") or "unknown"),
        synthetic=bool(raw.get("synthetic", False)),
    )
