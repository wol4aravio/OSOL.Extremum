import numpy as np
import torch

def constrain_point(x, min_value, max_value):
	return np.clip(x, min_value, max_value)

def constrain_tensor(x, min_value, max_value):
	return x.clamp(min=min_value, max=max_value)