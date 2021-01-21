"""Streamlit App for Animation Demonstration."""

import os

import plotly.io as pio
import streamlit as st

st.set_page_config(layout="wide")

st.header("OSOL.Extremum: Solution Demonstration")

query_param_run_id = st.experimental_get_query_params()["run_id"][0]


@st.cache(suppress_st_warning=True)
def load_frames(run_id):
    """Load drames for specified run_id"""
    frames_locations = ".optimizer/{}".format(run_id)
    frames = list()
    for frame_name in sorted(os.listdir(frames_locations)):
        with open(frames_locations + "/{}".format(frame_name), "r") as file:
            frames.append("\n".join(file.readlines()))
    return frames


frames_for_the_run = load_frames(query_param_run_id)

slider = st.slider(
    "Iteration ID",
    min_value=0,
    max_value=(len(frames_for_the_run) - 1),
    value=0,
)
st.plotly_chart(pio.from_json(frames_for_the_run[slider]))
