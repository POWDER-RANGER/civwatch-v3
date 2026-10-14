"""Minimal ADB discovery: only devices explicitly authorized by Android are returned."""
import shutil
import subprocess


def get_connected_devices() -> list[str]:
    adb = shutil.which("adb")
    if not adb:
        return []
    try:
        result = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    devices = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices
