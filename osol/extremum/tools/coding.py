import json

import numpy


class EncodeFromNumpy(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, numpy.ndarray):
            return {"_kind_": "ndarray", "_value_": o.tolist()}
        if isinstance(o, numpy.integer):
            return int(o)
        if isinstance(o, numpy.floating):
            return float(o)
        if isinstance(o, range):
            value = list(o)
            return {"_kind_": "range", "_value_": [value[0], value[-1] + 1]}
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
        if kind == "range":
            value = obj["_value_"]
            return range(value[0], value[-1])
        return obj
