"""Optimizer application."""

import json

import streamlit as st

from osol.extremum.applications.optimizer_tools import (
    generate_target_function_input,
    generate_variables_input,
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
    uploaded_file = st.file_uploader(
        "Upload function via file", type=["opt", "json"]
    )
    if uploaded_file is not None:
        problem = json.load((uploaded_file))
        target_function = generate_target_function_input(
            placeholder_function, problem["function"]
        )
        variables = generate_variables_input(
            placeholder_variables, ", ".join(problem["vars"])
        )
    if target_function != "" and variables != "":
        variables_list = [
            v for v in variables.replace(" ", "").split(",") if v != ""
        ]
        st.latex(
            "f({vars}) = {func}".format(
                vars=", ".join(variables_list), func=target_function
            )
        )
