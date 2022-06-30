# Pose-Estimate-As-Library
the wrapper libraries for pose estimate based on [mmpose](https://github.com/open-mmlab/mmpose).

# base library

This package is a wrapper of [mmpose](https://github.com/open-mmlab/mmpose).

And [pytorch](https://pytorch.org/) is used in mmpose.


# Usage


## 1. installation

## Estimate

You can execute pose-estimation with only few lines codes.

The API of mmpose is quite complex and it requires a lot of configuration. And config of mmpose is written on .py file.

So it is difficult to use mmpose as third-party library.


Pose-Estimate-As-Library helps you use mmpose with simple code, and setting by json format. 

sample code
```python
from epose.estimator import HRNetEstimator
import matplotlib.pyplot as plt

estimator = HRNetEstimator(
    posemodel_config_path="config/HRNet.json",
    detmodel_config_path="config/FasterRCNN.json",
    trained_det_model_path="https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth",
    trained_pose_model_path="https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"
)

pose_results, returned_outputs = estimator.estimate_from_imgfile(img_path="data/000000397133.jpg")
result_img = estimator.visualize_result(img_path="data/000000397133.jpg", pose_results=pose_results)

plt.imshow(result_img)
```


![result image](https://github.com/yushiokamura/pose-estimate-as-library/blob/feature/pypi/data/result_sample.jpg)