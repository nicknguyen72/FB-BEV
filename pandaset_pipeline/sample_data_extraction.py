import os
import json
import uuid

# NOTE: MAKE SURE TO RUN ALL LISTED FILES BEFORE RUNNING THIS SCRIPT
# sensor_extraction.py, calibrated_sensor_extraction.py, ego_pose_extraction.py, sample_extraction.py, annotation_extraction.py, sample_data_extraction.py

# Define paths
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
CAMERA_ROOT = os.path.join("data", "pandaset", "camera", "camera")


# Load all required JSONs
with open(os.path.join(OUTPUT_DIR, "sensor.json")) as f:
    sensor_data = json.load(f)
with open(os.path.join(OUTPUT_DIR, "calibrated_sensor.json")) as f:
    calibrated_data = json.load(f)
with open(os.path.join(OUTPUT_DIR, "ego_pose.json")) as f:
    ego_pose_data = json.load(f)
with open(os.path.join(OUTPUT_DIR, "sample.json")) as f:
    sample_data = json.load(f)
with open(os.path.join(OUTPUT_DIR, "frame_token_map.json")) as f:
    frame_token_map = json.load(f)

# Build lookup dictionaries
sensor_token_map = {s["channel"]: s["token"] for s in sensor_data}
calibrated_token_map = {c["sensor_token"]: c["token"] for c in calibrated_data}
ego_pose_lookup = {e["timestamp"]: e["token"] for e in ego_pose_data}

# Mapping of folders to nuScenes channel names
camera_channels = {
    "front_camera": "CAM_FRONT",
    "front_left_camera": "CAM_FRONT_LEFT",
    "front_right_camera": "CAM_FRONT_RIGHT",
    "left_camera": "CAM_LEFT",
    "right_camera": "CAM_RIGHT",
    "back_camera": "CAM_BACK"
}

# Build sample_data.json entries
sample_data_entries = []
for folder_name, channel_name in camera_channels.items():
    folder_path = os.path.join(CAMERA_ROOT, folder_name)
    timestamps_path = os.path.join(folder_path, "timestamps.json")
    if not os.path.exists(timestamps_path):
        print(f"WARNING --- Missing timestamps.json in {folder_path}")
        continue

    with open(timestamps_path) as f:
        timestamps = json.load(f)

    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".jpg")])
    sensor_token = sensor_token_map[channel_name]
    calibrated_token = calibrated_token_map[sensor_token]

    for i, img_file in enumerate(image_files):
        frame_id = f"{i:02d}"
        sample_token = frame_token_map.get(frame_id)
        if not sample_token or i >= len(timestamps):
            continue

        timestamp = int(timestamps[i] * 1e6)
        ego_pose_token = ego_pose_lookup.get(timestamp)
        if not ego_pose_token:
            continue

        entry = {
            "token": str(uuid.uuid4()),
            "sample_token": sample_token,
            "ego_pose_token": ego_pose_token,
            "calibrated_sensor_token": calibrated_token,
            "sensor_token": sensor_token,
            "filename": f"samples/{channel_name}/{img_file}",
            "timestamp": timestamp
        }
        sample_data_entries.append(entry)

# Save output
output_path = os.path.join(OUTPUT_DIR, "sample_data.json")
try:
    with open(output_path, "w") as f:
        json.dump(sample_data_entries, f, indent=2)
    print(f"SUCESSFUL --- sample_data.json generated with {len(sample_data_entries)} entries and saved to {output_path}")
except Exception as e:
    print(f"ERROR --- Failed to write sample_data.json: {e}")
