import os
import json
import uuid

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define source folder for timestamps and poses
FRONT_CAMERA_DIR = os.path.join("data", "pandaset", "camera", "camera", "front_camera")
TIMESTAMPS_PATH = os.path.join(FRONT_CAMERA_DIR, "timestamps.json")
POSES_PATH = os.path.join(FRONT_CAMERA_DIR, "poses.json")
EGO_POSE_OUTPUT = os.path.join(OUTPUT_DIR, "ego_pose.json")

# Load timestamps and poses
try:
    with open(TIMESTAMPS_PATH) as f:
        timestamps = json.load(f)
    with open(POSES_PATH) as f:
        poses = json.load(f)
except Exception as e:
    print(f"ERROR --- Failed to load pose or timestamp data: {e}")
    timestamps, poses = [], []

# Construct ego pose entries
ego_pose_entries = []
for ts, pose in zip(timestamps, poses):
    entry = {
        "token": str(uuid.uuid4()),
        "rotation": [
            pose["heading"]["w"],
            pose["heading"]["x"],
            pose["heading"]["y"],
            pose["heading"]["z"]
        ],
        "translation": [
            pose["position"]["x"],
            pose["position"]["y"],
            pose["position"]["z"]
        ],
        "timestamp": int(ts * 1e6)  # convert seconds to microseconds
    }
    ego_pose_entries.append(entry)

# Save to file
try:
    with open(EGO_POSE_OUTPUT, "w") as f:
        json.dump(ego_pose_entries, f, indent=2)
    print(f"SUCCESSFUL --- ego_pose.json generated with {len(ego_pose_entries)} entries at {EGO_POSE_OUTPUT}")
except Exception as e:
    print(f"ERROR --- Failed to write ego_pose.json: {e}")
