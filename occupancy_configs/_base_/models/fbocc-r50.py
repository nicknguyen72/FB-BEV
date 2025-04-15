# Simplified fbocc-r50.py model config for PandaSet

model = dict(
    type='FBOCC',
    img_backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN2d', requires_grad=True),
        norm_eval=True,
        style='pytorch'
    ),
    img_neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=4
    ),
    # pts_bbox_head=dict(
    #     type='OccHead',
    #     # bev_h=128,
    #     # bev_w=128,
    #     # bev_z=8,
    #     num_classes=18,
    #     loss_seg=dict(
    #         type='CrossEntropyLoss',
    #         use_sigmoid=False,
    #         loss_weight=1.0,
    #         ignore_index=255
    #     )
    # )
)

# Optional test_cfg (some tools expect this to exist)
test_cfg = dict(
    type='MultiScaleFlipAug3D',
    img_scale=(1600, 900)
)
