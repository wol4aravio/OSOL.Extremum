"""Optimizer application."""

import json

import numpy as np
import streamlit as st

from osol.extremum.algorithms.termination import (
    TerminationViaMaxCalls,
    TerminationViaMaxTime,
)
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

algorithm, problem = st.beta_columns(2)

with algorithm:
    algorithm_name = st.selectbox(
        "Algorithm", options=["FPA: Flower Pollination Algorithm"]
    )
    if algorithm_name.startswith("FPA:"):
        algorithm = generate_settings_fpa()

with problem:
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
    if target_function != "" and variables != "":
        variables_list = [v for v in parse_variable_input(variables) if v != ""]
        variables_list_str = ", ".join(variables_list)
        st.latex("f({v}) = {f}".format(v=variables_list_str, f=target_function))
        function = OptTask(
            {"function": target_function, "vars": variables_list}
        )
        search_area = np.array(json.loads("[{}]".format(search_area)))

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
    result = algorithm.optimize(function, search_area, number_of_iter)

if result is not None:
    st.text(str(result.tolist()))
