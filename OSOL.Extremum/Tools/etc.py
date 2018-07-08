def constrain_point(x, min_value, max_value):
    if x < min_value:
        return min_value
    elif x > max_value:
        return max_value
    else:
        return x
