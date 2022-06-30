# -*- coding: utf-8 -*-
"""Pose Estimation Modules
"""

import json
import numpy as np
from mmdet.models import build_detector
from mmdet.apis import inference_detector
from mmpose.models import build_posenet
from mmpose.apis import (inference_top_down_pose_model,
                         vis_pose_result, process_mmdet_results)
from mmcv.runner import load_checkpoint

from epose import Cfg


class BasePoseEstimator:
    def __init__(self,
                 posemodel_config_path: str,
                 detmodel_config_path: str,
                 trained_det_model_path: str,
                 trained_pose_model_path: str,
                 dataset_name: str = None,
                 map_location: str = "cpu") -> None:

        self._loadconf(detmodel_config_path, "detcfg")
        self._loadconf(posemodel_config_path, "posecfg")

        self._del_pretrained()

        self.det_model = self._build_detection_model(
            trained_det_model_path, map_location=map_location)
        self.pose_model = self._build_pose_model(
            trained_pose_model_path, map_location=map_location)

        if not dataset_name:
            self.dataset = self.posecfg.data.test["type"]

    def _del_pretrained(self):
        if hasattr(self, "posecfg"):
            if hasattr(self.posecfg, "model"):
                if hasattr(self.posecfg.model, "pretrained"):
                    self.posecfg.model["pretrained"] = None
                    self.posecfg.model.pretrained = None

    def estimate_pose_from_imgfile(self, img_path: str, cat_id: int = 1):
        """estimate pose from image file
        Args:
            img_path(str):input image path
            cat_id(int):category id in COCO dataset. 1 means person.
        Returns:
            pose_results(list of dict): results of estimation.
                each elements is  dict, and contains
                `bbox` and `keypoints` keys.
            returned_outputs(list of dict): the heatmatps of pose estimation.
        """

        person_results = self.estimate_person(img_path, cat_id=cat_id)

        pose_results, returned_outputs = inference_top_down_pose_model(
            self.pose_model,
            img_path,
            person_results,
            bbox_thr=0.3,
            format='xyxy',
            return_heatmap=True
        )

        return pose_results, returned_outputs

    def estimate_person(self, img_path: str, cat_id: int = 1):
        """
        """
        det_results = inference_detector(self.det_model, img_path)
        person_results = process_mmdet_results(det_results, cat_id=cat_id)
        return person_results

    def visualize_result(self,
                         img_path,
                         pose_results=None,
                         cat_id: int = 1,
                         dataset: str = "TopDownCocoDataset",
                         with_estimate: bool = False) -> np.array:

        if with_estimate:
            pose_results, _ = self.estimate_pose_from_imgfile(
                img_path=img_path, cat_id=cat_id)
        else:
            if pose_results is None:
                raise ValueError("")
        return_img = \
            vis_pose_result(
                self.pose_model,
                img_path,
                pose_results,
                dataset=dataset,
                show=False)
        return return_img

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

    def _build_pose_model(self, trained_model_path, map_location):
        """
        """
        pose_model = build_posenet(self.posecfg.model)
        _ = load_checkpoint(
            pose_model,
            trained_model_path,
            map_location=map_location
        )
        _ = pose_model.eval()
        pose_model.cfg = self.posecfg

        return pose_model
