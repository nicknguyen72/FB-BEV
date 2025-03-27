import os
import gzip
import pickle
import pandas as pd
import json
import uuid
import numpy as np

# NOTE: MAKE SURE TO sample_extraction.py FIRST BEFORE RUNNING THIS SCRIPT

# Base output directory
OUTPUT_DIR = os.path.join("pandaset_pipeline", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to the annotation files
CUBOID_PATH = "data/pandaset/annotations/annotations/cuboids"
FRAME_TOKEN_MAP_PATH = os.path.join(OUTPUT_DIR, "frame_token_map.json")

# Load frame_token_map.json to translate frame ID to sample_token
try:
    with open(FRAME_TOKEN_MAP_PATH, "r") as f:
        frame_token_map = json.load(f)
except Exception as e:
    print(f"ERROR --- Failed to load frame_token_map.json: {e}")
    frame_token_map = {}

# Function to convert yaw to quaternion (assuming roll = pitch = 0)
def yaw_to_quaternion(yaw):
    qw = np.cos(yaw / 2)
    qz = np.sin(yaw / 2)
    return [qw, 0.0, 0.0, qz]  # [w, x, y, z]

# Function to extract and combine all annotation cuboid data
def extract_all_annotations(cuboid_folder):
    combined_data = []
    for file in sorted(os.listdir(cuboid_folder)):
        if file.endswith('.pkl.gz'):
            file_path = os.path.join(cuboid_folder, file)
            with gzip.open(file_path, 'rb') as f:
                df = pickle.load(f)
                df['frame'] = file.replace('.pkl.gz', '')  # Add frame identifier
                combined_data.append(df)
    return pd.concat(combined_data, ignore_index=True)

# Function to convert DataFrame to nuScenes-style sample_annotations
def convert_to_nuscenes_annotations(df):
    sample_annotations = []
    for _, row in df.iterrows():
        frame_id = row["frame"]
        sample_token = frame_token_map.get(frame_id)
        if not sample_token:
            continue  # skip if token is not found

        annotation = {
            "token": str(uuid.uuid4()),
            "instance_token": row["uuid"],
            "sample_token": sample_token,
            "translation": [row["position.x"], row["position.y"], row["position.z"]],
            "size": [row["dimensions.x"], row["dimensions.y"], row["dimensions.z"]],
            "rotation": yaw_to_quaternion(row["yaw"]),
            "attribute_tokens": [row["attributes.object_motion"]] if pd.notnull(row["attributes.object_motion"]) else [],
            "visibility_token": "1",  # Placeholder
            "num_lidar_pts": None,
            "num_radar_pts": None
        }
        sample_annotations.append(annotation)
    return sample_annotations

# Main logic
if __name__ == "__main__":
    df = extract_all_annotations(CUBOID_PATH)
    annotations = convert_to_nuscenes_annotations(df)

    output_path = os.path.join(OUTPUT_DIR, "sample_annotations.json")
    try:
        with open(output_path, 'w') as f:
            json.dump(annotations, f, indent=2)
        print(f"SUCCESSFUL --- Extracted {len(annotations)} annotations and saved to {output_path}")
    except Exception as e:
        print(f"ERROR --- Failed to write output file: {e}")
