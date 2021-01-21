"""Set of tools for drawing."""

import numpy as np
import plotly.graph_objects as go


def draw_opt_task_2d(function, grid, points_x=101, points_y=101):
    """Draws contour plot for 2D function."""
    x_range = np.linspace(grid[0, 0], grid[0, 1], num=points_x)
    y_range = np.linspace(grid[1, 0], grid[1, 1], num=points_y)
    z_values = np.zeros(shape=(points_y, points_x))
    for i, y in enumerate(y_range):
        for j, x in enumerate(x_range):
            z_values[i, j] = function(x, y)
    return go.Contour(
        x=x_range, y=y_range, z=z_values, colorscale="turbo", showscale=False
    )


def make_animation_2d(contour, grid, df_animation):
    """Creates frames for 2D animation."""
    frames = list()
    for iteration_id in df_animation["iteration_id"].unique():
        df = df_animation.query("iteration_id == {}".format(iteration_id))
        frame = go.Figure(
            data=[contour, go.Scatter(x=df["x_1"], y=df["x_2"], mode="markers")]
        )
        frame.update_layout(
            xaxis=dict(range=[grid[0, 0], grid[0, 1]], autorange=False)
        )
        frame.update_layout(
            yaxis=dict(range=[grid[1, 0], grid[1, 1]], autorange=False)
        )
        frames.append(frame)
    return frames
