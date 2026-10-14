from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
import json
from datetime import datetime
from config import config
from acquisition.normalizer import normalize_observation
from acquisition.android_cellular import get_cellular_obs
from acquisition.simulator import generate_simulated_obs
from acquisition.adb_client import get_connected_devices
from inference.evidence_chain import sign_observation
from storage.database import save_observation, get_recent_anomalies
from inference.correlator import Correlator
from spatial.topology import topology
import uvicorn

app = FastAPI(
    title="CivWatch v3.0 - RF Observability",
    description="Reference dashboard. Synthetic samples are clearly labeled and are not RF detections.",
)


@app.get("/api/health")
async def health():
    devices = get_connected_devices()
    return {
        "status": "ok",
        "service": "civwatch-v3",
        "role": "reference_only",
        "connected_device_count": len(devices),
        "observation_mode": "device_metadata" if devices else "synthetic_demo",
        "canonical_rf_service": "https://github.com/POWDER-RANGER/civwatch-cell-titan",
        "system_of_record": "https://github.com/POWDER-RANGER/CivilianIntelligence",
    }


@app.get("/api/capabilities")
async def capabilities():
    return {
        "schema_version": "1.0",
        "service": "civwatch-v3",
        "role": "predecessor_reference_only",
        "domains": [
            {"id": "cellular", "available_mode": "Android device-reported metadata when an authorized ADB device is attached", "measurement_class": "device_reported_metadata"},
            {"id": "wifi", "available_mode": "not validated as physical capture in this reference service", "measurement_class": "reference_or_demo"},
            {"id": "d2d", "available_mode": "synthetic/reference only", "measurement_class": "synthetic"},
            {"id": "transport", "available_mode": "synthetic/reference only", "measurement_class": "synthetic"},
        ],
        "limitations": [
            "A phone system metadata is not raw baseband or spectrum capture",
            "Synthetic samples are not real-world detections",
            "Scores and flags are not proof of an interceptor or malicious activity",
            "Use CIVWATCH Cell Titan for the canonical RF service contract",
        ],
    }
correlator = Correlator()

# Mount static files for dashboard
app.mount("/static", StaticFiles(directory="presentation"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("presentation/dashboard.html", "r") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            devices = get_connected_devices()
            domain = "cellular"
            
            if devices:
                domain_data = get_cellular_obs(devices[0])
                observation_mode = "device_metadata"
            else:
                domain_data = generate_simulated_obs(domain)
                observation_mode = "synthetic_demo"

            obs_raw = {
                "sensor_id": config.SENSOR_ID,
                "timestamp": datetime.utcnow().isoformat(),
                "domain": domain,
                "observation_mode": observation_mode,
                "synthetic": observation_mode == "synthetic_demo",
                "payload": domain_data,
                "score": domain_data.get("score"),
                "flags": domain_data.get("flags", []),
                "confidence": domain_data.get("confidence")
            }
            
            normalized = normalize_observation(obs_raw, "cellular", config.SENSOR_ID)
            signed = sign_observation({**normalized.dict(), "observation_mode": observation_mode, "synthetic": observation_mode == "synthetic_demo"})
            save_observation(signed)
            
            correlated = correlator.correlate([signed])
            signed.update(correlated)
            
            await websocket.send_text(json.dumps(signed))
            await asyncio.sleep(3)
    except Exception as e:
        print(f"WS Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)