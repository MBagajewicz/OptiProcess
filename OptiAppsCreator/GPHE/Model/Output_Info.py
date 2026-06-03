##################################################################################################################
# region Titles and Header
# Nature: Post-optimization output calculations for GPHE — computes thermo/hydraulic/economics
#         derived values from optimal variables and model parameters.
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          02-Jun-2026     OptiAppsCreator           Initial version
##################################################################################################################
# INPUT:
#   build_output_info(optimal_vars, params, objective=None)
#     optimal_vars : dict  — discrete variable optimal values (Ntp, Pl, Sa, Nph, Npc)
#     params       : dict  — Model_Parameters submitted by user or merged with Example1
#     objective    : dict  — objective function info from extract_results() (optional)
#   Returns:
#     {
#       "objective": dict | None,
#       "calculations": { "vh": ..., "vc": ..., "DPh": ..., "DPc": ..., ... }
#     }
##################################################################################################################
# endregion
##################################################################################################################

import json
import numpy as np
from scipy import optimize


def _scalar(val):
    """Extract scalar from numpy array or return as-is if already scalar."""
    if isinstance(val, np.ndarray):
        return val.item()
    return float(val) if isinstance(val, (np.floating, np.integer)) else val


def build_output_info(optimal_vars, params, objective=None):
    """Compute thermo/hydraulic/economics output details for GPHE."""

    from GPHE.Calculations import (
        Calculations_GPHE_velocity,
        Calculations_GPHE_Reynolds,
        Calculations_GPHE_hh,
        Calculations_GPHE_hc,
        Calculations_GPHE_DeltaP_channel,
        Calculations_GPHE_DeltaP_port,
        Calculations_GPHE_U,
        Calculations_GPHE_epsilon_Nutcalc,
        Calculations_GPHE_correction_factor,
        Calculations_GPHE_area,
        Calculations_GPHE_CAPEX,
    )
    from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD

    Ntp = np.atleast_1d(float(optimal_vars["Ntp"]))
    Pl = int(optimal_vars["Pl"])
    Sa = np.atleast_1d(float(optimal_vars["Sa"]))
    Nph = np.atleast_1d(float(optimal_vars["Nph"]))
    Npc = np.atleast_1d(float(optimal_vars["Npc"]))

    Lp = params["ppLp"][Pl]
    Lw = params["ppLw"][Pl]
    Dp = params["ppDp"][Pl]
    bp = params["bp"]
    phi = params["phi"]
    thk = params["thk"]
    kplate = params["kplate"]

    mh = params["mh"]
    mc = params["mc"]
    roh = params["roh"]
    roc = params["roc"]
    Cph = params["Cph"]
    Cpc = params["Cpc"]
    mih = params["mih"]
    mic = params["mic"]
    kh = params["kh"]
    kc = params["kc"]
    Rfh = params["Rfh"]
    Rfc = params["Rfc"]
    Thi = params["Thi"]
    Tho = params["Tho"]
    Tci = params["Tci"]
    Tco = params["Tco"]
    DPhdisp = params["DPhdisp"]
    DPcdisp = params["DPcdisp"]

    vh = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Nph, bp, mh, roh)
    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, bp, mc, roc)

    Reh = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Nph, bp, phi, roh, mih, mh)
    Rec = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Npc, bp, phi, roc, mic, mc)

    hh = Calculations_GPHE_hh.GPHE_hh(Ntp, Lp, Lw, Nph, Sa, bp, phi, kh, Cph, mih, roh, mh)
    hc = Calculations_GPHE_hc.GPHE_hc(Ntp, Lw, Npc, Sa, bp, phi, kc, Cpc, mic, roc, mc)

    DPh_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(
        Ntp, Lp, Lw, Dp, Nph, Sa, bp, phi, roh, mih, mh)
    DPh_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, mh, roh)
    DPh_total = DPh_c + DPh_p

    DPc_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(
        Ntp, Lp, Lw, Dp, Npc, Sa, bp, phi, roc, mic, mc)
    DPc_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, mc, roc)
    DPc_total = DPc_c + DPc_p

    U_dirty = Calculations_GPHE_U.GPHE_overall_coefficient(
        Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi,
        Cpc, Cph, mic, mih, kc, kh, roc, roh, mc, mh)
    U_clean = Calculations_GPHE_U.GPHE_overall_coefficient(
        Ntp, Lp, Lw, Npc, Sa, Nph, 0.0, 0.0, thk, kplate, bp, phi,
        Cpc, Cph, mic, mih, kc, kh, roc, roh, mc, mh)

    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)

    xo = np.array([1, 0.8, 0.9])
    xsol = optimize.root(
        Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc,
        xo, args=(mh, Cph, Thi, Tho, Tci, mc, Cpc))
    F1_2 = (Thi - Tho) / LMTD / xsol.x[0]
    F = Calculations_GPHE_correction_factor.GPHE_correction_factor(Thi, Tho, Tci, Tco, Nph, Npc, F1_2)

    NTP_termicos = int(Ntp) - 2
    A_total = Calculations_GPHE_area.GPHE_area(phi, NTP_termicos, Lp, Lw)

    par_a = params.get("par_a", 0)
    par_b = params.get("par_b", 1)
    CAPEX = Calculations_GPHE_CAPEX.GPHE_CAPEX(Ntp, Lp, Lw, par_a, par_b, phi)

    pc = params.get("pc", 0)
    Nop = params.get("Nop", 0)
    eta = params.get("eta", 1)
    Cop_h = Nop * (pc / 1000) * (DPh_total * mh / (eta * roh))
    Cop_c = Nop * (pc / 1000) * (DPc_total * mc / (eta * roc))
    OPEX_total = Cop_h + Cop_c

    int_rate = params.get("int_rate", 0.1)
    n_years = params.get("n", 10)
    r = (int_rate * (1 + int_rate) ** n_years) / ((1 + int_rate) ** n_years - 1) if int_rate > 0 else 1.0 / n_years
    TAC = r * CAPEX + OPEX_total

    A_req = Q / (U_dirty * LMTD * F) if U_dirty > 0 and F > 0 else 0
    A_ratio = A_total / A_req if A_req > 0 else 0
    Q_kW = Q / 1000.0

    calculations = {
        "vh": _scalar(vh), "vc": _scalar(vc),
        "Reh": _scalar(Reh), "Rec": _scalar(Rec),
        "hh": _scalar(hh), "hc": _scalar(hc),
        "DPh_total": _scalar(DPh_total), "DPc_total": _scalar(DPc_total),
        "DPh": _scalar(DPh_total), "DPc": _scalar(DPc_total),
        "DPh_channel": _scalar(DPh_c), "DPc_channel": _scalar(DPc_c),
        "DPh_port": _scalar(DPh_p), "DPc_port": _scalar(DPc_p),
        "U": _scalar(U_dirty), "Uc": _scalar(U_clean),
        "F": _scalar(F),
        "LMTD": _scalar(LMTD),
        "A_total": _scalar(A_total),
        "A_req": _scalar(A_req),
        "A_ratio": _scalar(A_ratio),
        "CAPEX": _scalar(CAPEX), "OPEX_h": _scalar(Cop_h),
        "OPEX_c": _scalar(Cop_c), "OPEX_total": _scalar(OPEX_total),
        "TAC": _scalar(TAC), "Q": _scalar(Q_kW),
        "Ntp": int(Ntp), "NTP_termicos": int(NTP_termicos),
        "Pl": int(Pl), "Sa": int(Sa), "Nph": int(Nph), "Npc": int(Npc),
        "Lp": _scalar(Lp), "Lw": _scalar(Lw), "Dp": _scalar(Dp),
    }

    return {
        "objective": objective,
        "calculations": calculations,
    }


def write_output_json(output_info, output_path):
    """Write output_info dict to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_info, f, indent=2, ensure_ascii=False, default=str)
