import json
import numpy as np
from PIL import Image
from mmdet.models import build_detector
from mmpose.models import build_posenet
from mmpose.apis import inference_top_down_pose_model, vis_pose_result
from mmcv.runner import load_checkpoint

from epose import Cfg


class BasePoseEstimator:
    def __init__(self,
                 posemodel_config_path: str,
                 detmodel_config_path: str,
                 trained_det_model_path: str) -> None:

        self._loadconf(detmodel_config_path, "detcfg")
        self._loadconf(posemodel_config_path, "posecfg")

        self.det_model = self._build_detection_model(trained_det_model_path)

    def predict_from_imgfile(self, path: str):
        pass

    def predict_from_tensor(self, img):
        pass

    def predict_from_array(self, img):
        pass

    def visualize_result(self):
        pass

    def _load_pose_weight(self, checkpoint_pass):
        pass

    def _loadconf(self, configpath, mode="posecfg"):

        if mode not in ["posecfg", "detcfg"]:
            raise ValueError(
                f'argment arg must be `posecfg` or `detcfg`, but got {mode}')

        with open(configpath) as f:
            cfg = Cfg(json.load(f))
            setattr(self, mode, cfg)

    def _build_detection_model(self, trained_model_path, map_location):
        det_model = build_detector(self.detcfg.model)

        _ = load_checkpoint(det_model,
                            trained_model_path,
                            map_location=map_location
                            )
        det_model.to(map_location)
        det_model.eval()
        det_model.cfg = self.detcfg

        return det_model
