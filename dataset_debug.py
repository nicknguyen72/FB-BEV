# from mmcv import Config
# from mmdet3d.datasets import build_dataset
# import os
# import copy
# import pprint
# import torch

# print("🔧 Loading config...")
# cfg = Config.fromfile('occupancy_configs/fb_occ/fbocc-r50-pandaset-infer.py')

# print("📂 Building dataset...")
# dataset = build_dataset(cfg.data.test)

# print("📦 Fetching one sample with __getitem__...")

# try:
#     sample = dataset[0]
#     print("✅ dataset[0] succeeded.")
#     print("🖨️ Sample keys:", list(sample.keys()))

#     try:
#         pprint.pprint(sample, width=120)
#     except Exception as e:
#         print(f"⚠️ Pretty-printing failed: {e}")
# except RecursionError as e:
#     print(f"❌ RecursionError while accessing dataset[0]: {e}")
# except Exception as e:
#     print(f"❌ Other error while accessing dataset[0]: {e}")

import json

with open("data/pandaset_nuscenes_format/sample.json", "r") as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
print("Keys of first item:")
print(data[0].keys())
