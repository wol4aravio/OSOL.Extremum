"""Set of tools for Optimizer application."""


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


def parse_variable_input(variables):
    """Parse text input with comma delimited variables."""
    return variables.replace(" ", "").split(",")
