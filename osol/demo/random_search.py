"""Demo app: Random Search."""

import plotly.graph_objects as go
import streamlit as st
from osol.algorithms.random_search import RandomSearch
from osol.demo.misc import DEMO_FUNCTIONS, SEARCH_AREA, generate_contours

intro = st.markdown(
    """
# Random Search
## Description

Random Search (RS) is probably one of the simplest optimization techniques.
The procedure starts with a random point that is sampled from search area.
It is treated as possible solution.
Then it checks randomly selected points
that are located close to the possible solution.
If the selected point is better than the current solution
then it becomes new possible solution and all process is repeated.
"""
)

eps = st.slider(
    label="eps",
    min_value=1e-3,
    max_value=1.0,
    value=1e-1,
    step=1e-3,
    format="%.3f",
)

num_iter = st.number_input(
    label="Number of iterations",
    min_value=100,
    max_value=10_000,
    value=1_000,
    step=100,
)

rs = RandomSearch(eps)

target_function_name = st.selectbox(
    label="Target function", options=[f.name for f in DEMO_FUNCTIONS]
)

target_function = [
    f for f in DEMO_FUNCTIONS if f.name == target_function_name
][0]
contours = generate_contours(target_function, SEARCH_AREA)

optimize = st.button("Optimize")

if optimize:
    with st.spinner("Performing optimization"):
        result = rs.optimize(
            target_function, SEARCH_AREA, num_iter, save_trace=True
        )
        trace = getattr(result, "trace")

        frame = go.Figure(data=contours)
        frame.add_trace(
            go.Scatter(
                x=[point["x"][0] for point in trace],
                y=[point["x"][1] for point in trace],
            )
        )
        frame.update_layout(
            autosize=False, width=600, height=600,
        )

        st.plotly_chart(frame)

markdown_etc = st.markdown(
    """
## Benchmarking

## Applied Tasks

## References

"""
)
