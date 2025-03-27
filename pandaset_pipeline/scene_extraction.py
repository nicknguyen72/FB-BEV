import os
import json
import uuid

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load sample.json to determine first and last samples
SAMPLE_PATH = os.path.join(OUTPUT_DIR, "sample.json")
SCENE_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "scene.json")

try:
    with open(SAMPLE_PATH, "r") as f:
        samples = json.load(f)
except Exception as e:
    print(f"ERROR --- Failed to load sample.json: {e}")
    samples = []

# Sort by timestamp to determine start and end frames
samples_sorted = sorted(samples, key=lambda x: x["timestamp"])

# Create a single scene entry
scene_entry = {
    "token": str(uuid.uuid4()),
    "name": "scene-0001",
    "description": "Converted from PandaSet",
    "log_token": "placeholder",
    "first_sample_token": samples_sorted[0]["token"] if samples_sorted else None,
    "last_sample_token": samples_sorted[-1]["token"] if samples_sorted else None
}

# Save scene.json
try:
    with open(SCENE_OUTPUT_PATH, "w") as f:
        json.dump([scene_entry], f, indent=2)
    print(f"SUCESSFUL --- scene.json generated with 1 entry at {SCENE_OUTPUT_PATH}")
except Exception as e:
    print(f"ERRROR --- Failed to write scene.json: {e}")
