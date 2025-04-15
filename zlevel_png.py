import os
import numpy as np
import matplotlib.pyplot as plt

z = int(input("Enter the z-level (e.g., 0-15): "))


# Input predictions directory
vis_dir = "tmp_vis"  # change if needed

# Output PNGs directory
png_dir = "zlevel_pngs"
os.makedirs(png_dir, exist_ok=True)

# Number of predictions to visualize
num_to_plot = 80

for i in range(num_to_plot):
    npy_path = os.path.join(vis_dir, f"pred_{i:03d}.npy")
    if os.path.exists(npy_path):
        pred = np.load(npy_path, allow_pickle=True)

        # If it's a dictionary, unwrap it
        if isinstance(pred.item(), dict):
            pred = pred.item()
            if 'pred_occupancy' in pred:
                pred = pred['pred_occupancy']
            else:
                print(f"No 'pred_occupancy' key in {npy_path}")
                continue

        if pred.ndim == 3:
            slice_img = pred[:, :, z]
            plt.figure(figsize=(6, 6))
            plt.imshow(slice_img.T, cmap='tab20', origin='lower')
            plt.title(f"Prediction Slice - Frame {i:03d} (z={z})")
            plt.axis('off')
            plt.tight_layout()
            out_png = os.path.join(png_dir, f"pred_{i:03d}_{z:02d}.png")
            plt.savefig(out_png)
            plt.close()
            print(f"Saved {out_png}")
        else:
            print(f"Unexpected shape in {npy_path}: {pred.shape}")
    else:
        print(f"{npy_path} does not exist.")



