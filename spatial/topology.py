"""No location is inferred; topology is empty until measured relative inputs exist."""
class RelativeTopology:
    def snapshot(self) -> dict:
        return {"nodes": [], "edges": [], "state": "unavailable", "reason": "no_relative_measurements"}


topology = RelativeTopology()
