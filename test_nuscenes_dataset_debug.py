# test_nuscenes_dataset_debug.py

from mmdet3d.datasets.nuscenes_dataset import NuScenesDataset
import pprint

# Minimal config — make sure this ann_file and data_root exist (you can use small test versions or mocks)
ann_file = 'data/pandaset_nuscenes_format/sample.json'
data_root = 'data/pandaset_nuscenes_format/'

# Dummy pipeline — just to instantiate without needing a full transform chain
dummy_pipeline = []

try:
    print("🔧 Instantiating NuScenesDataset...")
    dataset = NuScenesDataset(
        ann_file=ann_file,
        pipeline=dummy_pipeline,
        data_root=data_root,
        test_mode=True,
        modality=dict(use_camera=True, use_lidar=False),
        box_type_3d='LiDAR'
    )
    print("✅ Successfully created NuScenesDataset!")

    print("🔍 Trying to get first data sample with get_data_info()...")
    sample_info = dataset.get_data_info(0)

    print("✅ Sample returned! Safe summary:")
    for key in sample_info:
        print(f"  • {key}: type = {type(sample_info[key])}")

    print("\n🔬 Full pprint dump (safely skipping large keys)...")
    filtered = {k: v for k, v in sample_info.items() if k not in ['lidar2img', 'cam_positions']}
    pprint.pprint(filtered, width=120)

except Exception as e:
    print(f"❌ Caught exception during dataset test:\n{e}")
