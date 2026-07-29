#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          02-Jul-2026     ChatGPT                    Temperature-dependent property functions for SPHE_DT
##################################################################################################################
#endregion

#region Import Library
import math
import numpy as np
#endregion

#region Property helpers

def _as_output_type(value, template):
    """Return a Python float for scalar input and a numpy array for array input."""
    arr = np.asarray(value, dtype=float)
    if np.asarray(template).ndim == 0:
        return float(arr)
    return arr


def _clip(value, min_value=None, max_value=None):
    """Clip scalar or array values while preserving the original shape."""
    arr = np.asarray(value, dtype=float)
    if min_value is not None:
        arr = np.maximum(arr, min_value)
    if max_value is not None:
        arr = np.minimum(arr, max_value)
    return arr


def constant_property(value):
    """Return a property function with a constant value."""
    value = float(value)

    def property_function(T):
        arr = np.zeros_like(np.asarray(T, dtype=float)) + value
        return _as_output_type(arr, T)

    return property_function


def linear_property(reference_value, reference_temperature, slope, min_value=None, max_value=None):
    """Return p(T) = p_ref + slope * (T - T_ref), optionally clipped."""
    reference_value = float(reference_value)
    reference_temperature = float(reference_temperature)
    slope = float(slope)

    def property_function(T):
        arr = reference_value + slope * (np.asarray(T, dtype=float) - reference_temperature)
        arr = _clip(arr, min_value=min_value, max_value=max_value)
        return _as_output_type(arr, T)

    return property_function


def exponential_property(reference_value, reference_temperature, coefficient, min_value=None, max_value=None):
    """Return p(T) = p_ref * exp(coefficient * (T - T_ref)), optionally clipped."""
    reference_value = float(reference_value)
    reference_temperature = float(reference_temperature)
    coefficient = float(coefficient)

    def property_function(T):
        arr = reference_value * np.exp(coefficient * (np.asarray(T, dtype=float) - reference_temperature))
        arr = _clip(arr, min_value=min_value, max_value=max_value)
        return _as_output_type(arr, T)

    return property_function


def viscosity_exponential_from_reference(reference_value, reference_temperature, beta=0.02, min_value=1e-7, max_value=None):
    """Return a viscosity function that decreases when temperature increases."""
    return exponential_property(
        reference_value=reference_value,
        reference_temperature=reference_temperature,
        coefficient=-abs(float(beta)),
        min_value=min_value,
        max_value=max_value,
    )


def density_linear_from_reference(reference_value, reference_temperature, slope=-0.7, min_value=1.0, max_value=None):
    """Return a liquid-density function with a configurable thermal expansion slope."""
    return linear_property(
        reference_value=reference_value,
        reference_temperature=reference_temperature,
        slope=slope,
        min_value=min_value,
        max_value=max_value,
    )


def cp_linear_from_reference(reference_value, reference_temperature, slope=1.0, min_value=1.0, max_value=None):
    """Return a heat-capacity function with a mild linear temperature dependence."""
    return linear_property(
        reference_value=reference_value,
        reference_temperature=reference_temperature,
        slope=slope,
        min_value=min_value,
        max_value=max_value,
    )


def conductivity_linear_from_reference(reference_value, reference_temperature, slope=0.0, min_value=1e-4, max_value=None):
    """Return a thermal-conductivity function with optional linear temperature dependence."""
    return linear_property(
        reference_value=reference_value,
        reference_temperature=reference_temperature,
        slope=slope,
        min_value=min_value,
        max_value=max_value,
    )

#endregion

#region Built-in water-like functions

def water_density(T):
    """Approximate liquid-water density in kg/m3 for engineering screening."""
    T_arr = np.asarray(T, dtype=float)
    rho = -0.0031 * T_arr * T_arr - 0.1354 * T_arr + 1002.4
    rho = _clip(rho, min_value=1.0)
    return _as_output_type(rho, T)


def water_cp(T):
    """Approximate liquid-water heat capacity in J/(kg K) for engineering screening."""
    T_arr = np.asarray(T, dtype=float)
    cp = -0.000213 * T_arr**3 + 0.0383 * T_arr**2 - 1.87 * T_arr + 4206.0
    cp = _clip(cp, min_value=1.0)
    return _as_output_type(cp, T)


def water_viscosity(T):
    """Approximate liquid-water viscosity in Pa s for engineering screening."""
    T_arr = np.asarray(T, dtype=float)
    mu = 0.001445 * np.exp(-0.01927 * T_arr)
    mu = _clip(mu, min_value=1e-7)
    return _as_output_type(mu, T)


def water_thermal_conductivity(T):
    """Approximate liquid-water thermal conductivity in W/(m K) for engineering screening."""
    T_arr = np.asarray(T, dtype=float)
    k = 0.0012 * T_arr + 0.5804
    k = _clip(k, min_value=1e-4)
    return _as_output_type(k, T)

#endregion

#region Model-parameter interface

def get_property_function(m_p, aliases, constant_key):
    """Return a property callable from model parameters.

    Parameters
    ----------
    m_p : dict
        Model parameters.
    aliases : tuple[str, ...]
        Accepted keys for the callable function.
    constant_key : str
        Constant fallback key, e.g. 'Cph'.
    """
    for key in aliases:
        func = m_p.get(key)
        if callable(func):
            return func

    return constant_property(m_p[constant_key])


def get_stream_property_functions(m_p):
    """Return temperature-dependent property functions for hot and cold streams."""
    return {
        "hot_cp": get_property_function(m_p, ("hot_cp_func", "Cph_func"), "Cph"),
        "hot_density": get_property_function(m_p, ("hot_density_func", "roh_func"), "roh"),
        "hot_viscosity": get_property_function(m_p, ("hot_viscosity_func", "mih_func"), "mih"),
        "hot_conductivity": get_property_function(m_p, ("hot_conductivity_func", "kh_func"), "kh"),
        "cold_cp": get_property_function(m_p, ("cold_cp_func", "Cpc_func"), "Cpc"),
        "cold_density": get_property_function(m_p, ("cold_density_func", "roc_func"), "roc"),
        "cold_viscosity": get_property_function(m_p, ("cold_viscosity_func", "mic_func"), "mic"),
        "cold_conductivity": get_property_function(m_p, ("cold_conductivity_func", "kc_func"), "kc"),
    }


def representative_temperatures(m_p):
    """Return representative hot/cold temperatures for hydraulic constraints and TAC."""
    mode = m_p.get("SPHE_DT_property_temperature_mode", "target_average")

    if mode == "inlet":
        return float(m_p["Thi"]), float(m_p["Tci"])

    if mode == "target_average":
        return 0.5 * (float(m_p["Thi"]) + float(m_p["Tho"])), 0.5 * (float(m_p["Tci"]) + float(m_p["Tco"]))

    if isinstance(mode, dict):
        return float(mode.get("hot", m_p["Thi"])), float(mode.get("cold", m_p["Tci"]))

    raise ValueError("SPHE_DT_property_temperature_mode must be 'inlet', 'target_average', or a dict with hot/cold values.")


def representative_properties(m_p):
    """Return representative properties for non-distributed calculations."""
    funcs = get_stream_property_functions(m_p)
    Th_ref, Tc_ref = representative_temperatures(m_p)

    return {
        "Th_ref": Th_ref,
        "Tc_ref": Tc_ref,
        "Cph": float(funcs["hot_cp"](Th_ref)),
        "roh": float(funcs["hot_density"](Th_ref)),
        "mih": float(funcs["hot_viscosity"](Th_ref)),
        "kh": float(funcs["hot_conductivity"](Th_ref)),
        "Cpc": float(funcs["cold_cp"](Tc_ref)),
        "roc": float(funcs["cold_density"](Tc_ref)),
        "mic": float(funcs["cold_viscosity"](Tc_ref)),
        "kc": float(funcs["cold_conductivity"](Tc_ref)),
    }


def property_bounds(func, Tmin, Tmax, samples=25):
    """Return min and max property values over a temperature interval."""
    grid = np.linspace(float(Tmin), float(Tmax), int(samples))
    values = np.asarray(func(grid), dtype=float)
    return float(np.min(values)), float(np.max(values))


def enthalpy_change(cp_func, T_a, T_b, samples=101):
    """Return integral Cp(T) dT from T_a to T_b in J/kg."""
    T_a = float(T_a)
    T_b = float(T_b)
    if T_a == T_b:
        return 0.0

    grid = np.linspace(T_a, T_b, int(samples))
    cp_values = np.asarray(cp_func(grid), dtype=float)
    return float(np.trapz(cp_values, grid))

#endregion
