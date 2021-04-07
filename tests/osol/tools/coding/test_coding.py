import json

import numpy as np
import pytest

from osol.tools.coding import DecodeToNumpy, EncodeFromNumpy


@pytest.mark.parametrize("_", range(100))
def test_encode_decode(_):
    vector = np.random.uniform(0.0, 1.0, size=(5,))
    coded = json.dumps(vector, cls=EncodeFromNumpy)
    decoded = json.loads(coded, cls=DecodeToNumpy)
    assert np.sum((vector - decoded) ** 2) < 1e-12
