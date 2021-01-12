"""Set of tools for Optimizer application."""

import streamlit as st

from osol.extremum.algorithms.flower_pollination_algorithm import FPA


def generate_text_input(placeholder, label, value=None):
    """Generates text input in placeholder."""
    if value is None:
        value_ = ""
    else:
        value_ = value
    return placeholder.text_input(label, value_)


def generate_target_function_input(placeholder, value=None):
    """Generates target function input window."""
    label = "Target Function (LaTeX compatible)"
    return generate_text_input(placeholder, label, value)


def generate_variables_input(placeholder, value=None):
    """Generates variables input window."""
    label = "Variables (comma separeted list)"
    return generate_text_input(placeholder, label, value)


def generate_search_area_input():
    """Generates search area input window."""
    label = "Search Area ([x1_min, x1_max], [x2_min, x2_max], ...)"
    return generate_text_input(st.empty(), label)


def parse_variable_input(variables):
    """Parse text input with comma delimited variables."""
    return variables.replace(" ", "").split(",")


def generate_settings_fpa():
    """Generate list of settings for FPA algorithm."""
    N = st.number_input("N", min_value=3, max_value=None, value=10)
    p = st.number_input("p", min_value=0.0, max_value=1.0, value=0.2)
    gamma = st.number_input("gamma", min_value=0.01, max_value=1.0, value=0.1)
    lambda_ = st.number_input(
        "lambda", min_value=0.1, max_value=10.0, value=1.0, step=0.1
    )
    return FPA(N, p, gamma, lambda_)
