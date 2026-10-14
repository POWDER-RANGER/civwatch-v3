"""Small SQLite event store for the v3 local reference dashboard."""
import json
import sqlite3
from pathlib import Path
from config import config


def _database_path() -> str:
    prefix = "sqlite:///"
    url = config.DB_URL
    if not url.startswith(prefix):
        raise RuntimeError("Reference v3 supports SQLite only; configure DATABASE_URL=sqlite:///./civwatch.db")
    path = url[len(prefix):]
    return str(Path(path))


def init_db() -> None:
    path = _database_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                domain TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )"""
        )
        conn.commit()


def save_observation(observation: dict) -> None:
    init_db()
    with sqlite3.connect(_database_path()) as conn:
        conn.execute(
            "INSERT INTO observations(sensor_id, timestamp, domain, payload_json) VALUES (?, ?, ?, ?)",
            (
                str(observation.get("sensor_id", "unknown"))[:128],
                str(observation.get("timestamp", ""))[:64],
                str(observation.get("domain", "unknown"))[:32],
                json.dumps(observation, sort_keys=True, separators=(",", ":"), default=str),
            ),
        )
        conn.commit()


def get_recent_anomalies(limit: int = 100) -> list[dict]:
    init_db()
    with sqlite3.connect(_database_path()) as conn:
        rows = conn.execute(
            "SELECT payload_json FROM observations ORDER BY id DESC LIMIT ?",
            (max(1, min(int(limit), 500)),),
        ).fetchall()
    return [json.loads(row[0]) for row in rows]
