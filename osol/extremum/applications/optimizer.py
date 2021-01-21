"""Optimizer application."""

import hashlib
import json
import os

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

from osol.extremum.algorithms.flower_pollination_algorithm import FPA
from osol.extremum.algorithms.termination import (
    TerminationViaMaxCalls,
    TerminationViaMaxTime,
)
from osol.extremum.applications.draw import draw_opt_task_2d, make_animation_2d
from osol.extremum.applications.optimizer_tools import (
    generate_search_area_input,
    generate_settings_fpa,
    generate_target_function_input,
    generate_variables_input,
    parse_variable_input,
)
from osol.extremum.tools.parser import OptTask

result = None

st.set_page_config(layout="wide")

st.header("OSOL.Extremum: Optimizer")

col_algorithm, col_problem, col_function = st.beta_columns(3)

with col_algorithm:
    algorithm_name = st.selectbox(
        "Algorithm", options=["FPA: Flower Pollination Algorithm"]
    )
    if algorithm_name.startswith("FPA:"):
        algorithm = generate_settings_fpa()

with col_problem:
    placeholder_function = st.empty()
    target_function = generate_target_function_input(placeholder_function)
    placeholder_variables = st.empty()
    variables = generate_variables_input(placeholder_variables)
    search_area = generate_search_area_input()
    uploaded_file = st.file_uploader("Upload function via file", types=["json"])
    if uploaded_file is not None:
        problem = json.load((uploaded_file))
        target_function = generate_target_function_input(
            placeholder_function, problem["function"]
        )
        variables = generate_variables_input(
            placeholder_variables, ", ".join(problem["vars"])
        )

if target_function != "" and variables != "" and search_area != "":
    total_function_string = target_function + variables + search_area
    function_id = hashlib.md5(total_function_string.encode()).hexdigest()
    function_filename = ".optimizer/{}.json".format(function_id)
    os.makedirs(os.path.dirname(function_filename), exist_ok=True)
    variables_list = [v for v in parse_variable_input(variables) if v != ""]
    variables_list_str = ", ".join(variables_list)
    search_area = np.array(json.loads("[{}]".format(search_area)))
    function = OptTask({"function": target_function, "vars": variables_list})
    with col_function:
        placeholder_function_latex = st.empty()
        placeholder_function_plot = st.empty()
        if not os.path.exists(function_filename):
            contour = go.Figure(draw_opt_task_2d(function, search_area))
            with open(function_filename, "w") as file:
                file.write(contour.to_json(pretty=True))
        else:
            with open(function_filename, "r") as file:
                contour = pio.from_json("\n".join(file.readlines()))
        placeholder_function_latex.latex(
            "f({v}) = {f}".format(v=variables_list_str, f=target_function)
        )
        if len(variables_list) == 2:
            placeholder_function_plot.plotly_chart(
                contour, use_container_width=True
            )

term_max_iter, term_max_calls, term_max_time = st.beta_columns(3)

with term_max_iter:
    number_of_iter = st.number_input(
        "Number of iterations", value=1, min_value=1
    )

with term_max_calls:
    number_of_calls = st.number_input(
        "Max number of calls (zero means infinity)", value=0, min_value=0
    )

with term_max_time:
    number_of_seconds = st.number_input(
        "Max number of seconds (zero means infinity)", value=0, min_value=0
    )

button_optimize = st.button("Optimize")
if button_optimize:
    progress_value = 0.0
    if number_of_calls > 0:
        function.add_termination_criterion(
            TerminationViaMaxCalls(number_of_calls)
        )
    if number_of_seconds > 0:
        function.add_termination_criterion(
            TerminationViaMaxTime(number_of_seconds)
        )

    def get_total_progress(progress_widget, criteria):
        """Refreshing callback."""
        progress_widget.progress(max(c.get_completeness() for c in criteria))

    function.add_callback(
        lambda f: get_total_progress(progress_bar, f.termination_criteria)
    )
    progress_bar = st.progress(progress_value)
    result, states = algorithm.optimize(
        function, search_area, number_of_iter, serialize_states=True
    )
    if algorithm_name.startswith("FPA:"):
        df_animation = FPA.convert_states_to_animation_df(states)
        frames = make_animation_2d(contour.data[0], search_area, df_animation)
    if len(variables_list) == 2:
        run_id = hashlib.md5(str(np.random.uniform()).encode()).hexdigest()
        frames_location = ".optimizer/{}".format(run_id)
        os.makedirs(frames_location, exist_ok=True)
        for frame_id, frame in enumerate(frames):
            with open(
                frames_location + "/{:07d}.json".format(frame_id + 1), "w"
            ) as file:
                file.write(frame.to_json(pretty=True))

if result is not None:
    st.markdown("Solution: `" + str(result.tolist()) + "`")
    if len(variables_list) == 2:
        st.markdown("[Demo Link](http://0.0.0.0:8502?run_id=" + run_id + ")")
