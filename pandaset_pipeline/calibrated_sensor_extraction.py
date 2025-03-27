import json
import os
import uuid

# NOTE: MAKE SURE TO sensor_extraction.py FIRST BEFORE RUNNING THIS SCRIPT

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping of camera folder to nuScenes channel name
camera_map = {
    "front_camera": "CAM_FRONT",
    "front_left_camera": "CAM_FRONT_LEFT",
    "front_right_camera": "CAM_FRONT_RIGHT",
    "left_camera": "CAM_LEFT",
    "right_camera": "CAM_RIGHT",
    "back_camera": "CAM_BACK"
}

# Path to your dataset and sensor.json
CAMERA_ROOT = os.path.join("data", "pandaset", "camera", "camera")
SENSOR_JSON_PATH = os.path.join(OUTPUT_DIR, "sensor.json")
CALIBRATED_SENSOR_PATH = os.path.join(OUTPUT_DIR, "calibrated_sensor.json")

# Load sensor.json
try:
    with open(SENSOR_JSON_PATH, 'r') as f:
        sensors = json.load(f)
except Exception as e:
    print(f"Failed to load sensor.json: {e}")
    sensors = []

sensor_token_map = {s["channel"]: s["token"] for s in sensors}

# Build calibrated_sensor.json entries
calibrated_sensors = []
for folder, channel_name in camera_map.items():
    folder_path = os.path.join(CAMERA_ROOT, folder)
    try:
        with open(os.path.join(folder_path, "poses.json")) as pf:
            poses = json.load(pf)
        with open(os.path.join(folder_path, "intrinsics.json")) as inf:
            intr = json.load(inf)

        first_pose = poses[0]

        calibrated_entry = {
            "token": str(uuid.uuid4()),
            "sensor_token": sensor_token_map[channel_name],
            "translation": [
                first_pose["position"]["x"],
                first_pose["position"]["y"],
                first_pose["position"]["z"]
            ],
            "rotation": [
                first_pose["heading"]["w"],
                first_pose["heading"]["x"],
                first_pose["heading"]["y"],
                first_pose["heading"]["z"]
            ],
            "camera_intrinsic": [
                [intr["fx"], 0.0, intr["cx"]],
                [0.0, intr["fy"], intr["cy"]],
                [0.0, 0.0, 1.0]
            ]
        }
        calibrated_sensors.append(calibrated_entry)

    except Exception as e:
        print(f"WARNING --- Skipping {folder} due to error: {e}")

# Save calibrated_sensor.json
try:
    with open(CALIBRATED_SENSOR_PATH, "w") as f:
        json.dump(calibrated_sensors, f, indent=2)
    print(f"SUCESSFUL --- Saved calibrated_sensor.json with {len(calibrated_sensors)} entries to {CALIBRATED_SENSOR_PATH}")
except Exception as e:
    print(f"ERROR --- Failed to write calibrated_sensor.json: {e}")
