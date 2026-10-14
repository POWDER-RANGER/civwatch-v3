"""Conservative correlation placeholder; one event is not a correlation."""
class Correlator:
    def correlate(self, observations: list[dict]) -> dict:
        if len(observations) < 2:
            return {
                "correlation": {
                    "status": "insufficient_observations",
                    "count": len(observations),
                    "anomaly_claim": False,
                }
            }
        return {
            "correlation": {
                "status": "reference_only_not_validated",
                "count": len(observations),
                "anomaly_claim": False,
            }
        }
