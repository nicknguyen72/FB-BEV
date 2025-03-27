import json
import uuid
import os

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping from PandaSet camera folder names to nuScenes channel names
camera_map = {
    "front_camera": "CAM_FRONT",
    "front_left_camera": "CAM_FRONT_LEFT",
    "front_right_camera": "CAM_FRONT_RIGHT",
    "left_camera": "CAM_LEFT",
    "right_camera": "CAM_RIGHT",
    "back_camera": "CAM_BACK"
}

# Generate sensor.json entries
sensor_json = []
for original, mapped in camera_map.items():
    entry = {
        "token": str(uuid.uuid4()),  # unique identifier for this sensor
        "channel": mapped,           # nuScenes standard camera channel name
        "modality": "camera"         # sensor type
    }
    sensor_json.append(entry)

# Save to file
output_path = os.path.join(OUTPUT_DIR, "sensor.json")
try:
    with open(output_path, "w") as f:
        json.dump(sensor_json, f, indent=2)
    print(f"SUCESSFUL --- Generated sensor.json with {len(sensor_json)} cameras and saved to {output_path}")
except Exception as e:
    print(f"ERROR --- Failed to write sensor.json: {e}")
