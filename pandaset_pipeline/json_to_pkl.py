import json
import pickle
from pathlib import Path

# Set base camera path and output path
base_path = Path("/scratch/group/occupany_network_cap/test1/FB-BEV/data/pandaset/camera/camera")
output_pkl_path = Path("/scratch/group/occupany_network_cap/test1/FB-BEV/data/pandaset_nuscenes_format/bevdetv2-nuscenes_infos_val.pkl")

# Camera mapping
cam_map = {
    "front_camera": "CAM_FRONT",
    "front_left_camera": "CAM_FRONT_LEFT",
    "front_right_camera": "CAM_FRONT_RIGHT",
    "back_camera": "CAM_BACK",
    "left_camera": "CAM_BACK_LEFT",
    "right_camera": "CAM_BACK_RIGHT",
}

# Use timestamps from one camera (they're all synced)
with open(base_path / "right_camera" / "timestamps.json", "r") as f:
    timestamps = json.load(f)

info_entries = []

# Iterate over each timestamp
for idx, ts in enumerate(timestamps):
    token = f"{idx:02d}"
    scene_name = f"{idx:04d}"
    entry = {
        "token": token,
        "timestamp": ts,
        "cams": {},
        "lidar2ego_translation": [0, 0, 0],
        "lidar2ego_rotation": [1, 0, 0, 0],
        "ego2global_translation": [0, 0, 0],
        "ego2global_rotation": [1, 0, 0, 0],
        "prev": "",
        "next": "",
        "lidar_path": "data/unused/placeholder.bin",
        "sweeps": [],
        "scene_name": scene_name,
        "lidarseg_filename": "None"
    }

    for folder, cam in cam_map.items():
        cam_path = base_path / folder
        image_name = f"{idx:02d}.jpg"
        image_path = f"data/pandaset/camera/camera/{folder}/{image_name}"

        # Load pose and intrinsics
        with open(cam_path / "poses.json", "r") as f:
            pose = json.load(f)[idx]
        with open(cam_path / "intrinsics.json", "r") as f:
            intr = json.load(f)

        entry["cams"][cam] = {
            "data_path": image_path,
            "sensor2ego_translation": [
                pose["position"]["x"],
                pose["position"]["y"],
                pose["position"]["z"]
            ],
            "sensor2ego_rotation": [
                pose["heading"]["w"],
                pose["heading"]["x"],
                pose["heading"]["y"],
                pose["heading"]["z"]
            ],
            "ego2global_translation": [0, 0, 0],
            "ego2global_rotation": [1, 0, 0, 0],
            "cam_intrinsic": [
                [intr["fx"], 0, intr["cx"]],
                [0, intr["fy"], intr["cy"]],
                [0, 0, 1]
            ]
        }

    info_entries.append(entry)

# Save new PKL
with open(output_pkl_path, "wb") as f:
    pickle.dump({
        "infos": info_entries,
        "metadata": {
            "version": "v1.0-custom"
        }
    }, f)

print(f"? Saved: {output_pkl_path} with {len(info_entries)} entries")
for i, entry in enumerate(info_entries): 
  print(f"\nEntry {i}:") 
  print(json.dumps(entry, indent=2))