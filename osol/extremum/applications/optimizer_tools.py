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
    return generate_text_input(
        placeholder, "Target Function (LaTeX compatible)", value
    )


def generate_variables_input(placeholder, value=None):
    """Generates variables input window."""
    return generate_text_input(
        placeholder, "Variables (comma separeted list)", value
    )
