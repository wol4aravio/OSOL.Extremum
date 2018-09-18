import numpy as np

def constrain_point(x, min_value, max_value):
	return np.clip(x, min_value, max_value)
