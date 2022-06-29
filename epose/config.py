

class Cfg(dict):
    def __init__(self, arg):
        super().__init__(arg)
        for k, v in arg.items():
            if "pipeline" in str(k):
                v = PipelineCfg(v)
                setattr(self, k, v)
            elif "dataset_info" in str(k):
                v = DatasetInfoCfg(v)
                setattr(self, k, v)
            elif type(v) == dict:
                setattr(self, str(k), Cfg(v))
                self[k] = Cfg(v)
            else:
                setattr(self, str(k), v)


class TransCfg(Cfg):
    tuple_keys = ["img_scale"]

    def __init__(self, arg):
        super().__init__(arg)
        for k, v in self.items():
            if k in TransCfg.tuple_keys:
                self._list2tuple(k, v)

    def _list2tuple(self, k, v):
        self[k] = tuple(v)


class PipelineCfg(list):
    def __init__(self, args):
        super().__init__(args)

        for i, item in enumerate(self):
            self[i] = TransCfg(item)


class DatasetInfoCfg(Cfg):
    key_point_key = "keypoint_info"

    def __init__(self, arg) -> None:
        super().__init__(arg)
        for k, v in arg.items():
            if k == DatasetInfoCfg.key_point_key:
                keypoint_indexs = [i for i in v.keys() if type(i) == str]
                for i in keypoint_indexs:
                    v[int(i)] = v.pop(str(i))

            if type(v) == dict:
                setattr(self, k, Cfg(v))
                self[k] = Cfg(v)
            else:
                setattr(self, k, v)
