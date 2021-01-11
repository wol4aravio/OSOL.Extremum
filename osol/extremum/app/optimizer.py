"""Optimizer application."""

import streamlit as st

st.set_page_config(layout="wide")

st.header("OSOL.Extremum: Optimizer")

algorithm, problem = st.beta_columns(2)

with algorithm:
    st.text("Algorithm Placeholder")

with problem:
    target_function = st.text_input("Target Function (LaTeX compatible)", "")
    variables = st.text_input("Variables (comma separeted list)", "")
    if target_function != "" and variables != "":
        variables_list = [
            v for v in variables.replace(" ", "").split(",") if v != ""
        ]
        st.latex(
            "f({vars}) = {func}".format(
                vars=", ".join(variables_list), func=target_function
            )
        )
