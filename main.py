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

app = FastAPI(title="CivWatch v3.0 - RF Observability")
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
            else:
                domain_data = generate_simulated_obs(domain)
            
            obs_raw = {
                "sensor_id": config.SENSOR_ID,
                "timestamp": datetime.utcnow().isoformat(),
                "domain": domain,
                "payload": domain_data,
                "score": domain_data.get("score", 65),
                "flags": domain_data.get("flags", []),
                "confidence": domain_data.get("confidence", 0.88)
            }
            
            normalized = normalize_observation(obs_raw, "cellular", config.SENSOR_ID)
            signed = sign_observation(normalized.dict())
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