###################################################################################################################
# region Titles and Header
# Nature: Constraints and objective function for the temperature-dependent distributed SPHE model
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva                Original SPHE formulation
#   0.1          02-Jul-2026     ChatGPT                    SPHE_DT branch with temperature-dependent properties
###################################################################################################################
#endregion

#region Import Library
from SPHE_DT.Calculations import (
    Calculations_SPHE_DT_Reynolds,
    Calculations_SPHE_DT_velocity,
    Calculations_SPHE_DT_correction_factor,
    Calculations_SPHE_DT_Area,
    Calculations_SPHE_DT_TAC,
    Calculations_SPHE_DT_DeltaP,
    Calculations_SPHE_DT_U,
    Calculations_SPHE_DT_Temp,
    Calculations_SPHE_DT_Properties,
)
from Common_Equations_HEX import Calculations_HEX_LMTD, Calculations_HEX_heatload
#endregion

#region Helpers

def _representative_properties(m_p):
    """Return representative properties for hydraulic constraints and TAC."""
    return Calculations_SPHE_DT_Properties.representative_properties(m_p)


def _property_functions(m_p):
    """Return temperature-dependent property functions from model parameters."""
    return Calculations_SPHE_DT_Properties.get_stream_property_functions(m_p)


def _distributed_temperature_outputs(L, H, ds, dh, dc, m_p):
    """Return hot and cold outlet temperatures from the nonlinear distributed model.

    The Set Trimming engine passes complete candidate vectors to each
    constraint. This helper broadcasts the design variables and evaluates the
    scalar temperature solver candidate by candidate. Scalar results are cached
    in Calculations_SPHE_DT_Temp.
    """
    import numpy as np

    funcs = _property_functions(m_p)
    M = int(m_p.get("SPHE_DT_solver_M", m_p.get("SPHE_D_solver_M", 8)))
    tol = float(m_p.get("SPHE_DT_solver_tol", 1e-6))
    max_iter = int(m_p.get("SPHE_DT_solver_max_iter", 50))
    relaxation = float(m_p.get("SPHE_DT_solver_relaxation", 0.7))

    L_arr, H_arr, ds_arr, dh_arr, dc_arr = np.broadcast_arrays(L, H, ds, dh, dc)

    Tho_calc = np.empty(L_arr.shape, dtype=float)
    Tco_calc = np.empty(L_arr.shape, dtype=float)

    for idx in np.ndindex(L_arr.shape):
        try:
            Tho_i, Tco_i, _, converged, _, _ = Calculations_SPHE_DT_Temp.SPHE_output_temperatures_from_length(
                L_arr[idx],
                H_arr[idx],
                ds_arr[idx],
                m_p["thk"],
                dh_arr[idx],
                dc_arr[idx],
                m_p["mh"],
                m_p["Thi"],
                m_p["Tci"],
                m_p["thk"],
                m_p["Rfh"],
                m_p["Rfc"],
                m_p["kplate"],
                funcs["hot_cp"],
                funcs["hot_density"],
                funcs["hot_viscosity"],
                funcs["hot_conductivity"],
                m_p["mc"],
                funcs["cold_cp"],
                funcs["cold_density"],
                funcs["cold_viscosity"],
                funcs["cold_conductivity"],
                M=M,
                tol=tol,
                max_iter=max_iter,
                relaxation=relaxation,
            )
            if not converged and m_p.get("SPHE_DT_require_convergence", False):
                Tho_i = 1e30
                Tco_i = -1e30
        except Exception:
            Tho_i = 1e30
            Tco_i = -1e30

        Tho_calc[idx] = Tho_i
        Tco_calc[idx] = Tco_i

    if Tho_calc.ndim == 0:
        return float(Tho_calc), float(Tco_calc)

    return Tho_calc, Tco_calc

#endregion

#region Constraints

def LH_lb(L, H, ds, dh, dc, m_p):
    """Lower bound on L/H."""
    return m_p["LBLH"] - L / H


def LH_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on L/H."""
    return L / H - m_p["UBLH"]


def vh_lb(L, H, ds, dh, dc, m_p):
    """Lower bound on hot-channel velocity."""
    props = _representative_properties(m_p)
    vh, _ = Calculations_SPHE_DT_velocity.SPHE_velocity(m_p["mh"], m_p["mc"], H, dh, dc, props["roh"], props["roc"])
    return m_p["vhmin"] - vh


def vh_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on hot-channel velocity."""
    props = _representative_properties(m_p)
    vh, _ = Calculations_SPHE_DT_velocity.SPHE_velocity(m_p["mh"], m_p["mc"], H, dh, dc, props["roh"], props["roc"])
    return vh - m_p["vhmax"]


def vc_lb(L, H, ds, dh, dc, m_p):
    """Lower bound on cold-channel velocity."""
    props = _representative_properties(m_p)
    _, vc = Calculations_SPHE_DT_velocity.SPHE_velocity(m_p["mh"], m_p["mc"], H, dh, dc, props["roh"], props["roc"])
    return m_p["vcmin"] - vc


def vc_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on cold-channel velocity."""
    props = _representative_properties(m_p)
    _, vc = Calculations_SPHE_DT_velocity.SPHE_velocity(m_p["mh"], m_p["mc"], H, dh, dc, props["roh"], props["roc"])
    return vc - m_p["vcmax"]


def Reh_lb(L, H, ds, dh, dc, m_p):
    """Lower bound on hot-channel Reynolds number."""
    props = _representative_properties(m_p)
    Reh, _, Reeh, _ = Calculations_SPHE_DT_Reynolds.SPHE_Reynolds(
        dh, dc, H, m_p["mh"], m_p["mc"], props["mih"], props["mic"], L, m_p["thk"], ds
    )
    return Reeh - Reh


def Rec_lb(L, H, ds, dh, dc, m_p):
    """Lower bound on cold-channel Reynolds number."""
    props = _representative_properties(m_p)
    _, Rec, _, Reec = Calculations_SPHE_DT_Reynolds.SPHE_Reynolds(
        dh, dc, H, m_p["mh"], m_p["mc"], props["mih"], props["mic"], L, m_p["thk"], ds
    )
    return Reec - Rec


def dltph_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on hot-channel pressure drop."""
    props = _representative_properties(m_p)
    dltph, _ = Calculations_SPHE_DT_DeltaP.SPHE_DeltaP(
        L, props["roh"], props["roc"], m_p["mh"], m_p["mc"], H, dh, dc, props["mih"], props["mic"]
    )
    return dltph - m_p["DPhdisp"]


def dltpc_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on cold-channel pressure drop."""
    props = _representative_properties(m_p)
    _, dltpc = Calculations_SPHE_DT_DeltaP.SPHE_DeltaP(
        L, props["roh"], props["roc"], m_p["mh"], m_p["mc"], H, dh, dc, props["mih"], props["mic"]
    )
    return dltpc - m_p["DPcdisp"]


def Areq(L, H, ds, dh, dc, m_p):
    """Legacy LMTD area constraint using representative temperature-dependent properties."""
    props = _representative_properties(m_p)
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p["mh"], props["Cph"], m_p["Thi"], m_p["Tho"])
    U = Calculations_SPHE_DT_U.SPHE_overall_coefficient(
        L,
        dh,
        dc,
        ds,
        H,
        m_p["thk"],
        m_p["mh"],
        m_p["mc"],
        props["mih"],
        props["mic"],
        props["Cph"],
        props["Cpc"],
        props["kh"],
        props["kc"],
        m_p["Rfh"],
        m_p["Rfc"],
        m_p["kplate"],
    )
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p["Thi"], m_p["Tho"], m_p["Tci"], m_p["Tco"])
    F = Calculations_SPHE_DT_correction_factor.SPHE_correction_factor(
        L,
        H,
        dh,
        dc,
        ds,
        m_p["thk"],
        m_p["mh"],
        m_p["mc"],
        props["mih"],
        props["mic"],
        props["Cph"],
        props["Cpc"],
        props["kh"],
        props["kc"],
        m_p["Rfh"],
        m_p["Rfc"],
        m_p["kplate"],
    )
    A = Calculations_SPHE_DT_Area.SPHE_area(L, H)
    Areq_value = Q / (U * LMTD * F)
    return (Areq_value * (1 + m_p["Aexc"] / 100)) - A


def Areq_screen(L, H, ds, dh, dc, m_p):
    """Optional fast LMTD screening constraint before the nonlinear distributed solver."""
    if not m_p.get("SPHE_DT_use_lmtd_screen", True):
        return -1.0
    return Areq(L, H, ds, dh, dc, m_p)


def Tho_ub_fast_screen(L, H, ds, dh, dc, m_p):
    """Optional cheap hot-outlet screen before the full nonlinear solve."""
    if not m_p.get("SPHE_DT_use_fast_temperature_screen", True):
        return -1.0

    original_M = m_p.get("SPHE_DT_solver_M")
    original_tol = m_p.get("SPHE_DT_solver_tol")
    original_max_iter = m_p.get("SPHE_DT_solver_max_iter")
    original_relaxation = m_p.get("SPHE_DT_solver_relaxation")

    try:
        m_p["SPHE_DT_solver_M"] = int(m_p.get("SPHE_DT_fast_screen_M", 2))
        m_p["SPHE_DT_solver_tol"] = float(m_p.get("SPHE_DT_fast_screen_tol", 1e-3))
        m_p["SPHE_DT_solver_max_iter"] = int(m_p.get("SPHE_DT_fast_screen_max_iter", 1))
        m_p["SPHE_DT_solver_relaxation"] = float(m_p.get("SPHE_DT_fast_screen_relaxation", 1.0))
        Tho_calc, _ = _distributed_temperature_outputs(L, H, ds, dh, dc, m_p)
    finally:
        if original_M is None:
            m_p.pop("SPHE_DT_solver_M", None)
        else:
            m_p["SPHE_DT_solver_M"] = original_M
        if original_tol is None:
            m_p.pop("SPHE_DT_solver_tol", None)
        else:
            m_p["SPHE_DT_solver_tol"] = original_tol
        if original_max_iter is None:
            m_p.pop("SPHE_DT_solver_max_iter", None)
        else:
            m_p["SPHE_DT_solver_max_iter"] = original_max_iter
        if original_relaxation is None:
            m_p.pop("SPHE_DT_solver_relaxation", None)
        else:
            m_p["SPHE_DT_solver_relaxation"] = original_relaxation

    screen_tol = m_p.get("SPHE_DT_screen_temp_tol", 10.0)
    return Tho_calc - m_p["Tho"] - screen_tol


def Tho_ub(L, H, ds, dh, dc, m_p):
    """Upper bound on calculated hot-stream outlet temperature."""
    try:
        Tho_calc, _ = _distributed_temperature_outputs(L, H, ds, dh, dc, m_p)
    except Exception:
        return 1e30

    tol = m_p.get("Temp_tol", 0.0)
    return Tho_calc - m_p["Tho"] - tol


def Tco_lb(L, H, ds, dh, dc, m_p):
    """Optional lower bound on calculated cold-stream outlet temperature."""
    try:
        _, Tco_calc = _distributed_temperature_outputs(L, H, ds, dh, dc, m_p)
    except Exception:
        return 1e30

    tol = m_p.get("Temp_tol", 0.0)
    return m_p["Tco"] - Tco_calc - tol

#endregion

#region Objective function

def SPHE_OF(L, H, ds, dh, dc, m_p):
    """Total annualized cost using representative temperature-dependent hydraulic properties."""
    props = _representative_properties(m_p)
    return Calculations_SPHE_DT_TAC.SPHE_TAC(
        m_p["int_rate"],
        m_p["n"],
        m_p["par_a"],
        m_p["par_b"],
        H,
        L,
        m_p["pc"],
        m_p["eta"],
        m_p["mh"],
        m_p["mc"],
        props["roh"],
        props["roc"],
        dh,
        dc,
        props["mih"],
        props["mic"],
        m_p["Nop"],
    )

#endregion
