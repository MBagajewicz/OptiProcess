##################################################################################################################
#region Titles and Header
# Nature: Parameters calculations for SPHE_DT
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini              Original SPHE parameter update
#   0.1          02-Jul-2026     ChatGPT                    Temperature-dependent property bounds
##################################################################################################################
#endregion

#region Import Library
import numpy as np
from SPHE_DT.Calculations import Calculations_SPHE_DT_Properties
#endregion

#region Parameters Calculation functions

def Parameter_Bounds(m_p):
    """Update representative properties and conservative property bounds."""
    funcs = Calculations_SPHE_DT_Properties.get_stream_property_functions(m_p)
    reps = Calculations_SPHE_DT_Properties.representative_properties(m_p)

    # Representative properties used by hydraulic constraints and objective function.
    m_p["Cph_ref"] = reps["Cph"]
    m_p["roh_ref"] = reps["roh"]
    m_p["mih_ref"] = reps["mih"]
    m_p["kh_ref"] = reps["kh"]
    m_p["Cpc_ref"] = reps["Cpc"]
    m_p["roc_ref"] = reps["roc"]
    m_p["mic_ref"] = reps["mic"]
    m_p["kc_ref"] = reps["kc"]

    Tmin = min(float(m_p["Thi"]), float(m_p["Tho"]), float(m_p["Tci"]), float(m_p["Tco"]))
    Tmax = max(float(m_p["Thi"]), float(m_p["Tho"]), float(m_p["Tci"]), float(m_p["Tco"]))
    samples = int(m_p.get("SPHE_DT_property_bound_samples", 25))

    hot_rho_min, hot_rho_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["hot_density"], Tmin, Tmax, samples)
    cold_rho_min, cold_rho_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["cold_density"], Tmin, Tmax, samples)
    hot_cp_min, hot_cp_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["hot_cp"], Tmin, Tmax, samples)
    cold_cp_min, cold_cp_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["cold_cp"], Tmin, Tmax, samples)
    hot_mu_min, hot_mu_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["hot_viscosity"], Tmin, Tmax, samples)
    cold_mu_min, cold_mu_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["cold_viscosity"], Tmin, Tmax, samples)
    hot_k_min, hot_k_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["hot_conductivity"], Tmin, Tmax, samples)
    cold_k_min, cold_k_max = Calculations_SPHE_DT_Properties.property_bounds(funcs["cold_conductivity"], Tmin, Tmax, samples)

    m_p["romin"] = min(hot_rho_min, cold_rho_min)
    m_p["romax"] = max(hot_rho_max, cold_rho_max)
    m_p["Cpmin"] = min(hot_cp_min, cold_cp_min)
    m_p["Cpmax"] = max(hot_cp_max, cold_cp_max)
    m_p["mimin"] = min(hot_mu_min, cold_mu_min)
    m_p["mimax"] = max(hot_mu_max, cold_mu_max)
    m_p["kmin"] = min(hot_k_min, cold_k_min)
    m_p["kmax"] = max(hot_k_max, cold_k_max)

    return m_p

#endregion
