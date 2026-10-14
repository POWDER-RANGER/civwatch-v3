"""Privacy-minimizing Android telephony metadata collector (not baseband capture)."""
import shutil
import subprocess


def get_cellular_obs(device: str) -> dict:
    adb = shutil.which("adb")
    if not adb or not device:
        return {
            "source": "android_adb",
            "measurement_class": "device_reported_metadata",
            "observed": False,
            "reason": "adb_or_authorized_device_unavailable",
            "score": None,
            "flags": [],
            "confidence": None,
        }
    try:
        result = subprocess.run(
            [adb, "-s", str(device), "shell", "dumpsys", "telephony.registry"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        result = None
    output = result.stdout if result and result.returncode == 0 else ""
    return {
        "source": "android_adb",
        "measurement_class": "device_reported_metadata",
        "observed": bool(output),
        "radio_metadata_available": bool(output),
        "raw_output_omitted": True,
        "score": None,
        "flags": [],
        "confidence": None,
        "limitations": [
            "System-reported metadata only; not raw baseband or spectrum capture",
            "No conclusion about interceptor presence or absence",
        ],
    }
