"""HMAC provenance stamp for reference events; not a public-key signature."""
import hashlib
import hmac
import json
import secrets
from config import config

# A configured key is required for stable signatures across restarts. If absent,
# a process-local key prevents a dangerous hard-coded default but is ephemeral.
_PROCESS_KEY = (config.SECRET_KEY or secrets.token_urlsafe(32)).encode("utf-8")


def sign_observation(observation: dict) -> dict:
    signed = dict(observation)
    material = json.dumps(signed, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    signed["provenance"] = {
        "algorithm": "HMAC-SHA256",
        "key_mode": "configured" if config.SECRET_KEY else "ephemeral_process_key",
        "digest": hmac.new(_PROCESS_KEY, material.encode("utf-8"), hashlib.sha256).hexdigest(),
        "verified": False,
    }
    return signed
