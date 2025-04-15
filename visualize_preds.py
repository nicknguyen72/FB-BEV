import cv2
import os
from pathlib import Path
from collections import defaultdict

# Specify the z-level you want to create a video for (e.g., "00", "01", ..., "15")
target_z = "00"

# Directory containing the PNGs
img_dir = Path("zlevel_pngs")
output_dir = Path("zlevel_videos")
output_dir.mkdir(exist_ok=True)

fps = 20  # Adjust playback speed

# Collect only PNGs for the specified z-level
img_paths = sorted([
    img_path for img_path in img_dir.glob("pred_*_*.png")
    if img_path.stem.split("_")[-1] == target_z
])

if not img_paths:
    print(f"No images found for z-level {target_z}")
else:
    # Read first image to get dimensions
    first_img = cv2.imread(str(img_paths[0]))
    height, width, _ = first_img.shape

    output_path = output_dir / f"z{target_z}_prediction_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    for img_path in img_paths:
        img = cv2.imread(str(img_path))
        writer.write(img)
        print(f"[z={target_z}] Added {img_path.name}")

    writer.release()
    print(f"? Video saved to {output_path}")


