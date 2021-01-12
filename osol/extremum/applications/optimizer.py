"""Optimizer application."""

import json

import streamlit as st

from osol.extremum.applications.optimizer_tools import (
    generate_target_function_input,
    generate_variables_input,
    parse_variable_input,
)

st.set_page_config(layout="wide")

st.header("OSOL.Extremum: Optimizer")

algorithm, problem = st.beta_columns(2)

with algorithm:
    st.text("Algorithm Placeholder")

with problem:
    placeholder_function = st.empty()
    target_function = generate_target_function_input(placeholder_function)
    placeholder_variables = st.empty()
    variables = generate_variables_input(placeholder_variables)
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
        variables_list = ", ".join(variables_list)
        st.latex("f({v}) = {f}".format(v=variables_list, f=target_function))
