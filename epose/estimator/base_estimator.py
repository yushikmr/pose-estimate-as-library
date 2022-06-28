import json
import numpy as np
from PIL import Image
from mmpose.models import build_posenet
from mmpose.apis import inference_top_down_pose_model, vis_pose_result

class BasePoseEstimator:
    def __init__(self, 
                posemodel_config:json, 
                detmodel_config:json) -> None:
        pass

    def predict_from_imgfile(self, path:str):
        pass

    def predict_from_tensor(self, img):
        pass

    def predict_from_array(self, img):
        pass

    def visualize_result(self):
        pass


    def _load_pose_weight(self, checkpoint_pass):
        pass