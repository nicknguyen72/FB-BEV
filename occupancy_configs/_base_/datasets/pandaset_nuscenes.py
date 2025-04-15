# Modified for PandaSet nuScenes-format dataset

data_root = 'data/pandaset_nuscenes_format/'
class_names = [
    'car', 'truck', 'construction_vehicle', 'bus', 'trailer',
    'barrier', 'motorcycle', 'bicycle', 'pedestrian', 'traffic_cone'
]
input_modality = {
    'use_lidar': False,
    'use_camera': True,
    'use_radar': False,
    'use_map': False,
    'use_external': False
}

file_client_args = dict(backend='disk')
