import os
import json
import uuid

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to front_camera timestamps.json (used for all frame timestamps)
TIMESTAMPS_PATH = os.path.join("data", "pandaset", "camera", "camera", "front_camera", "timestamps.json")
SAMPLE_JSON_PATH = os.path.join(OUTPUT_DIR, "sample.json")
FRAME_TOKEN_MAP_PATH = os.path.join(OUTPUT_DIR, "frame_token_map.json")

# Load timestamps
try:
    with open(TIMESTAMPS_PATH) as f:
        timestamps = json.load(f)
except Exception as e:
    print(f"ERROR --- Failed to load timestamps: {e}")
    timestamps = []

# Generate UUIDs and build frame-token map
sample_entries = []
frame_token_map = {}

for i, ts in enumerate(timestamps):
    frame_id = f"{i:02d}"  # "00", "01", etc.
    token = str(uuid.uuid4())
    frame_token_map[frame_id] = token

    entry = {
        "token": token,
        "timestamp": int(ts * 1e6),  # convert to microseconds
        "prev": None if i == 0 else None,  # to be updated
        "next": None,  # to be updated
        "scene_token": "placeholder"
    }
    sample_entries.append(entry)

# Update prev/next links
for i in range(len(sample_entries)):
    if i > 0:
        sample_entries[i]["prev"] = sample_entries[i - 1]["token"]
    if i < len(sample_entries) - 1:
        sample_entries[i]["next"] = sample_entries[i + 1]["token"]

# Save sample.json and frame_token_map.json
try:
    with open(SAMPLE_JSON_PATH, "w") as f:
        json.dump(sample_entries, f, indent=2)
    with open(FRAME_TOKEN_MAP_PATH, "w") as f:
        json.dump(frame_token_map, f, indent=2)
    print(f"SUCCESSFUL --- sample.json and frame_token_map.json saved with {len(sample_entries)} entries")
except Exception as e:
    print(f"ERRRO --- Failed to write sample or token map: {e}")
