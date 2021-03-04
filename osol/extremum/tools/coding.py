import json

import numpy


class EncodeFromNumpy(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, numpy.ndarray):
            return {"_kind_": "ndarray", "_value_": o.tolist()}
        return super().default(o)


class DecodeToNumpy(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=DecodeToNumpy.decoder_hook, *args, **kwargs
        )

    @staticmethod
    def decoder_hook(obj):
        if "_kind_" not in obj:
            return obj
        kind = obj["_kind_"]
        if kind == "ndarray":
            return numpy.array(obj["_value_"])
        return obj
