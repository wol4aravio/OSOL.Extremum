"""Optimizer application."""

import json

import numpy as np
import streamlit as st

from osol.extremum.applications.optimizer_tools import (
    generate_search_area_input,
    generate_settings_fpa,
    generate_target_function_input,
    generate_variables_input,
    parse_variable_input,
)
from osol.extremum.tools.parser import OptTask

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

number_of_iter = st.number_input("Number of iterations", min_value=1)
button_optimize = st.button("Optimize")
if button_optimize:
    result = algorithm.optimize(function, search_area, number_of_iter)
    st.text(str(result.tolist()))
