"""Helpers for model discrete variable standard values."""


def is_grouped_standard_values(values):
    return isinstance(values, dict)


def flatten_standard_values(values):
    if not is_grouped_standard_values(values):
        return values or []
    flattened = []
    for standard_values in values.values():
        if isinstance(standard_values, (list, tuple)):
            flattened.extend(standard_values)
    return flattened


def grouped_standard_options(values):
    if not is_grouped_standard_values(values):
        return None
    return {
        str(standard): list(standard_values or [])
        for standard, standard_values in values.items()
    }
