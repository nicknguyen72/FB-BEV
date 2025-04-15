import json
from collections import defaultdict
from pathlib import Path

# Load files
base_path = Path("/scratch/group/occupany_network_cap/test1/FB-BEV/pandaset_pipeline/outputs")
with open(base_path / "sensor.json") as f:
    sensor_data = {entry["token"]: entry for entry in json.load(f)}
with open(base_path / "calibrated_sensor.json") as f:
    calib_data = {entry["token"]: entry for entry in json.load(f)}
with open(base_path / "ego_pose.json") as f:
    ego_pose_data = {entry["token"]: entry for entry in json.load(f)}
with open(base_path / "sample_data.json") as f:
    sample_data_entries = json.load(f)
with open(base_path / "sample.json") as f:
    sample_entries = json.load(f)

# Group sample_data by sample_token and filter camera data
cams_by_sample = defaultdict(dict)
for entry in sample_data_entries:
    sensor = sensor_data[entry["sensor_token"]]
    if sensor["modality"] == "camera":
        channel = sensor["channel"]
        calib = calib_data[entry["calibrated_sensor_token"]]
        ego_pose = ego_pose_data[entry["ego_pose_token"]]

        cams_by_sample[entry["sample_token"]][channel] = {
            "data_path": entry["filename"],
            "sensor2ego_rotation": calib["rotation"],
            "sensor2ego_translation": calib["translation"],
            "ego2global_rotation": ego_pose["rotation"],
            "ego2global_translation": ego_pose["translation"],
            "timestamp": entry["timestamp"],
            "cam_intrinsic": calib.get("camera_intrinsic", [[1000, 0, 512], [0, 1000, 384], [0, 0, 1]]),

            # 🛠️ Fixed: Use identity matrix and zero vector
            "sensor2lidar_rotation": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]
            ],
            "sensor2lidar_translation": [0.0, 0.0, 0.0]
        }

# Patch sample.json entries
patched_samples = []
for sample in sample_entries:
    token = sample["token"]
    if token in cams_by_sample:
        sample["cams"] = cams_by_sample[token]
    patched_samples.append(sample)

# Save patched sample.json
patched_sample_path = base_path / "patched_sample.json"
with open(patched_sample_path, "w") as f:
    json.dump(patched_samples, f, indent=2)

print(f"✅ Patched sample.json written to: {patched_sample_path}")
