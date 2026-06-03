##################################################################################################################
# region Titles and Header
# Nature: Post-optimization output calculations for STHE — computes thermo/hydraulic/economics
#         derived values from optimal variables and model parameters.
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          02-Jun-2026     OptiAppsCreator           Extracted from solver_runner.py
##################################################################################################################
# INPUT:
#   build_output_info(optimal_vars, params, objective=None)
#     optimal_vars : dict  — discrete variable optimal values (Ds, dte, Npt, rp, lay, L, Nb, Bc)
#     params       : dict  — Model_Parameters submitted by user or merged with Example1
#     objective    : dict  — objective function info from extract_results() (optional)
#   Returns:
#     {
#       "objective": dict | None,
#       "calculations": { "vt": ..., "vs": ..., "Ret": ..., ... }
#     }
#
#   write_output_json(output_info, output_path)
#     output_info : dict  — result from build_output_info()
#     output_path : str   — file path for JSON output
##################################################################################################################
# endregion
##################################################################################################################

import json
import numpy as np


def _scalar(val):
    """Extract scalar from numpy array or return as-is if already scalar."""
    if isinstance(val, np.ndarray):
        return val.item()
    return float(val) if isinstance(val, (np.floating, np.integer)) else val


def build_output_info(optimal_vars, params, objective=None):
    """Compute thermo/hydraulic/economics output details for STHE."""

    from STHE.Model.Parameters_Update_STHE import allocation
    from STHE.Calculations import (
        Calculations_STHE_velocity_tubeside,
        Calculations_STHE_velocity_shellside,
        Calculations_STHE_Reynolds_tubeside,
        Calculations_STHE_Reynolds_shellside,
        Calculations_STHE_htubeside,
        Calculations_STHE_hshellside,
        Calculations_STHE_U,
        Calculations_STHE_DeltaPtubeside,
        Calculations_STHE_DeltaPshellside,
        Calculations_STHE_area,
        Calculations_STHE_correction_factor,
    )
    from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD

    Ds = np.atleast_1d(float(optimal_vars["Ds"]))
    dte = np.atleast_1d(float(optimal_vars["dte"]))
    Npt = np.atleast_1d(float(optimal_vars["Npt"]))
    rp = np.atleast_1d(float(optimal_vars["rp"]))
    lay = np.atleast_1d(float(optimal_vars["lay"]))
    L = np.atleast_1d(float(optimal_vars["L"]))
    Nb = np.atleast_1d(float(optimal_vars["Nb"]))
    Bc = np.atleast_1d(float(optimal_vars["Bc"]))

    m_p = allocation(dict(params))

    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(
        m_p["mt"], m_p["rot"], m_p["thk"], Ds, dte, Npt, rp, lay, m_p)
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(
        m_p["ms"], m_p["ros"], Ds, rp, L, Nb, dte, lay, m_p)

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(
        m_p["mt"], m_p["rot"], m_p["mit"], m_p["thk"], Ds, dte, Npt, rp, lay, m_p)
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(
        m_p["ms"], m_p["ros"], m_p["mis"], Ds, dte, rp, lay, L, Nb, m_p)

    ht = Calculations_STHE_htubeside.STHE_h_tubeside(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], m_p["thk"],
        m_p["yfluid"], Ds, dte, Npt, rp, lay, L, m_p)
    hs = Calculations_STHE_hshellside.STHE_h_shellside(
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    U_dirty = Calculations_STHE_U.STHE_overall_coefficient(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], m_p["Rft"],
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"], m_p["Rfs"],
        m_p["thk"], params.get("ktube", 50), m_p["yfluid"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    U_clean = Calculations_STHE_U.STHE_overall_coefficient(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], 0.0,
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"], 0.0,
        m_p["thk"], params.get("ktube", 50), m_p["yfluid"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(
        m_p["mt"], m_p["rot"], m_p["mit"], m_p["thk"], Ds, dte, Npt, rp, lay, L, m_p) / 1000.0
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(
        m_p["ms"], m_p["ros"], m_p["mis"], Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p) / 1000.0

    A_total = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)

    F = Calculations_STHE_correction_factor.STHE_correction_factor(
        params["Thi"], params["Tho"], params["Tci"], params["Tco"], Npt, params["Xp"])

    par_a = params.get("par_a", 0)
    par_b = params.get("par_b", 1)
    CAPEX = par_a * A_total ** par_b

    pc = params.get("pc", 0)
    Nop = params.get("Nop", 0)
    eta = params.get("eta", 1)
    DPt_Pa = DPt * 1000
    DPs_Pa = DPs * 1000
    Cop_t = Nop * (pc / 1000) * (DPt_Pa * m_p["mt"] / (eta * m_p["rot"]))
    Cop_s = Nop * (pc / 1000) * (DPs_Pa * m_p["ms"] / (eta * m_p["ros"]))
    OPEX_total = Cop_t + Cop_s

    int_rate = params.get("int_rate", 0.1)
    n_years = params.get("n", 10)
    r = (int_rate * (1 + int_rate) ** n_years) / ((1 + int_rate) ** n_years - 1) if int_rate > 0 else 1.0 / n_years
    TAC = r * CAPEX + OPEX_total

    Q = Calculations_HEX_heatload.HEX_heat_load(params["mh"], params["Cph"], params["Thi"], params["Tho"])
    Q_kW = Q / 1000.0

    denom = np.pi * _scalar(dte) * _scalar(L)
    Nt = int(round(_scalar(A_total) / denom)) if denom > 0 else 0

    LMTD = Calculations_HEX_LMTD.HEX_lmtd(
        params["Thi"], params["Tho"], params["Tci"], params["Tco"])
    A_req = Q / (_scalar(U_dirty) * _scalar(LMTD) * _scalar(F)) if _scalar(U_dirty) > 0 and _scalar(F) > 0 else 0
    A_ratio = _scalar(A_total) / A_req if A_req > 0 else 0

    calculations = {
        "vt": _scalar(vt), "vs": _scalar(vs),
        "Ret": _scalar(Ret), "Res": _scalar(Res),
        "ht": _scalar(ht), "hs": _scalar(hs),
        "U": _scalar(U_dirty), "Uc": _scalar(U_clean),
        "DPt": _scalar(DPt), "DPs": _scalar(DPs),
        "CAPEX": _scalar(CAPEX), "OPEX_t": _scalar(Cop_t),
        "OPEX_s": _scalar(Cop_s), "OPEX_total": _scalar(OPEX_total),
        "TAC": _scalar(TAC), "Q": _scalar(Q_kW),
        "Nt": Nt, "A_total": _scalar(A_total),
        "F": _scalar(F), "A_shell": _scalar(A_total), "A_ratio": _scalar(A_ratio),
    }

    return {
        "objective": objective,
        "calculations": calculations,
    }


def write_output_json(output_info, output_path):
    """Write output_info dict to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_info, f, indent=2, ensure_ascii=False, default=str)
