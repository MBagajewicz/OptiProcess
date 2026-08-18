###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          01-Dec-2024     Mariana Mello             Add constraints
#   0.3          03-Mar-2025     Mariana Mello             Changes after add options of tube and shell methods
#   0.4          23-Apr-2025     Mariana Mello             Update to fix error and add constraint Fmin
#   0.5          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)  for each constraint defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Active_Constraints_List']
# Then add an Objective Function to be minimized before declared in:
#                            Model_Declarations['Standard_Objective_Function']['Equation_Name']
# Finally, add the Lower Bound x
# endregion
############################################################################################

##################################################################################################################
# region Import Library
from Simulator_STHE.Calculations_STHE import (
    Calculations_STHE_Reynolds_tubeside,
    Calculations_STHE_velocity_tubeside,
    Calculations_STHE_Reynolds_shellside,
    Calculations_STHE_correction_factor,
    Calculations_STHE_velocity_shellside,
    Calculations_STHE_DeltaPshellside,
    Calculations_STHE_DeltaPtubeside,
    Calculations_STHE_area,
    Calculations_STHE_TAC,
    Calculations_STHE_CAPEX,
    Calculations_STHE_U
)
from Common.HEX_Calculations import Calculations_HEX_LMTD, Calculations_HEX_heatload
import numpy as np
# endregion
##################################################################################################################

##################################################################################################################
# region Constraints


def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on L/Ds
    fun_val = m_p['LBLD'] - L / Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on L/Ds
    fun_val = L / Ds - m_p['UBLD']
    return fun_val
def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = 0.2 * Ds - lbc
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = lbc - 1 * Ds
    return fun_val

def lbmax(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    lbc = (L / (Nb + 1))
    if m_p['Shell_Method'] == 'Bell':
        lbmax = (m_p['plbmax1']*dte + m_p['plbmax2'])*0.5
    elif m_p['Shell_Method'] == 'Kern':
        lbmax = lbc*1e10
    fun_val = lbc - lbmax
    return fun_val

def _shell_mass_flowrate(m_p, NSS, algn):
    """Return shell-side mass flow through one STHE unit.

    NSS and algn may be scalars or arrays of Set Trimming candidates.
    """
    NSS = np.asarray(NSS)
    algn = np.asarray(algn)
    if np.any(NSS < 1):
        raise ValueError("NSS must be greater than or equal to 1.")
    if np.any(~np.isin(algn, [0, 1, 2, 3])):
        raise ValueError("algn must contain only 0, 1, 2, or 3.")

    yfluid = m_p['yfluid']
    shell_is_parallel = (
        (algn == 1)
        | ((algn == 2) & (yfluid == 'hot_stream'))
        | ((algn == 3) & (yfluid == 'cold_stream'))
    )
    return np.where(shell_is_parallel, m_p['ms'] / NSS, m_p['ms'])


def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on vs
    ms_shell = _shell_mass_flowrate(m_p, NSS, algn)
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(
        ms_shell, m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p
    )
    fun_val = m_p['vsmin'] - vs
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on vs
    ms_shell = _shell_mass_flowrate(m_p, NSS, algn)
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(
        ms_shell, m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p
    )
    fun_val = vs - m_p['vsmax']
    return fun_val

def _tube_mass_flowrate(m_p, NSS, algn):
    """Return tube-side mass flow through one STHE unit.

    NSS and algn may be scalars or arrays of Set Trimming candidates.
    """
    NSS = np.asarray(NSS)
    algn = np.asarray(algn)
    if np.any(NSS < 1):
        raise ValueError("NSS must be greater than or equal to 1.")
    if np.any(~np.isin(algn, [0, 1, 2, 3])):
        raise ValueError("algn must contain only 0, 1, 2, or 3.")

    yfluid = m_p['yfluid']
    tube_is_parallel = (
        (algn == 1)
        | ((algn == 2) & (yfluid == 'cold_stream'))
        | ((algn == 3) & (yfluid == 'hot_stream'))
    )
    return np.where(tube_is_parallel, m_p['mt'] / NSS, m_p['mt'])


def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on vt
    mt_tube = _tube_mass_flowrate(m_p, NSS, algn)
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(
        mt_tube, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp, lay, m_p
    )
    #print('vt',vt)
    fun_val = m_p['vtmin'] - vt
    return fun_val

def vt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on vt
    mt_tube = _tube_mass_flowrate(m_p, NSS, algn)
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(
        mt_tube, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp, lay, m_p
    )
    fun_val = vt - m_p['vtmax']
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on Ret
    mt_tube = _tube_mass_flowrate(m_p, NSS, algn)
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(
        mt_tube, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp, lay, m_p
    )
    fun_val = m_p['Retmin'] - Ret
    return fun_val

def Ret_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on Ret
    mt_tube = _tube_mass_flowrate(m_p, NSS, algn)
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(
        mt_tube, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp, lay, m_p
    )
    fun_val = Ret - m_p['Retmax']
    return fun_val

def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Lower bound on Ret
    ms_shell = _shell_mass_flowrate(m_p, NSS, algn)
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(
        ms_shell, m_p['ros'], m_p['mis'], Ds, dte, rp, lay, L, Nb, m_p
    )
    fun_val = m_p['Resmin'] - Res
    return fun_val

def Res_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Upper bound on Res
    ms_shell = _shell_mass_flowrate(m_p, NSS, algn)
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(
        ms_shell, m_p['ros'], m_p['mis'], Ds, dte, rp, lay, L, Nb, m_p
    )
    fun_val = Res - m_p['Resmax']
    return fun_val

def _shell_series_count(m_p, NSS, algn):
    """Return number of shells crossed in series by shell-side stream."""
    NSS = np.asarray(NSS)
    algn = np.asarray(algn)
    if np.any(NSS < 1):
        raise ValueError("NSS must be greater than or equal to 1.")
    if np.any(~np.isin(algn, [0, 1, 2, 3])):
        raise ValueError("algn must contain only 0, 1, 2, or 3.")

    yfluid = m_p['yfluid']
    count = np.where(algn == 0, NSS, 1)
    count = np.where((algn == 2) & (yfluid == 'hot_stream'), NSS, count)
    count = np.where((algn == 3) & (yfluid == 'cold_stream'), NSS, count)
    return count


def _tube_series_count(m_p, NSS, algn):
    """Return number of shells crossed in series by tube-side stream."""
    NSS = np.asarray(NSS)
    algn = np.asarray(algn)
    if np.any(NSS < 1):
        raise ValueError("NSS must be greater than or equal to 1.")
    if np.any(~np.isin(algn, [0, 1, 2, 3])):
        raise ValueError("algn must contain only 0, 1, 2, or 3.")

    yfluid = m_p['yfluid']
    count = np.where(algn == 0, NSS, 1)
    count = np.where((algn == 2) & (yfluid == 'hot_stream'), NSS, count)
    count = np.where((algn == 3) & (yfluid == 'cold_stream'), NSS, count)
    return count


def DPs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Pressure drop through one shell
    ms_shell = _shell_mass_flowrate(m_p, NSS, algn)
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(
        ms_shell, m_p['ros'], m_p['mis'], Ds, dte, Npt, rp,
        lay, L, Nb, Bc, m_p
    )

    # Accumulate pressure drop when the shell-side stream crosses
    # multiple shells in series.
    DPs *= _shell_series_count(m_p, NSS, algn)

    fun_val = DPs - m_p['DPsdisp']
    return fun_val

def DPt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Pressure drop through one shell
    mt_tube = _tube_mass_flowrate(m_p, NSS, algn)
    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(
        mt_tube, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte,
        Npt, rp, lay, L, m_p
    )

    # Accumulate pressure drop when the tube-side stream crosses
    # multiple shells in series.
    DPt *= _tube_series_count(m_p, NSS, algn)

    fun_val = DPt - m_p['DPtdisp']
    return fun_val


def F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    F = Calculations_STHE_correction_factor.STHE_correction_factor(
        m_p['Thi'],
        m_p['Tho'],
        m_p['Tci'],
        m_p['Tco'],
        Npt,
        m_p['Xp']
    )
    fun_val = m_p['F_min'] - F
    return fun_val

def _F_total(Thi, Tho, Tci, Tco, Npt, NSS, algn, Xp):
    """
    Calculate the global LMTD correction factor for the complete
    multi-STHE configuration.

    The formulation is the direct translation of ApproachSelection.F_calc:
        algn = 0 -> S
        algn = 1 -> P
        algn = 2 -> SP (hot in series, cold in parallel)
        algn = 3 -> PS (hot in parallel, cold in series)

    The existing generic correction-factor library supplies the 1-shell
    / parallel factor F_1N. The additional S/SP/PS expressions are applied
    here because they belong to the global multi-STHE configuration.
    """


    # Preserve the generic library behavior for Npt == 1.
    if Npt <= 1:
        return 1.0

    # Common temperature parameters.
    R = (Thi - Tho) / (Tco - Tci)
    P = (Tco - Tci) / (Thi - Tci)

    Pmax = 2.0 / (R + 1.0 + (R**2 + 1.0)**0.5)

    # Same admissibility criterion used by ApproachSelection.F_calc.
    if not (Pmax * Xp > P):
        return 0.01

    # F_1N is already implemented in the generic library.
    F_1N = Calculations_STHE_correction_factor.STHE_correction_factor(
        Thi, Tho, Tci, Tco, Npt, Xp
    )
    
    # Parallel configuration: the global factor is F_1N.
    if algn == 1:
        return float(F_1N)

    # Single shell is also F_1N. This is particularly important for
    # the regression case NSS=1, algn=0.
    if NSS <= 1:
        return float(F_1N)

    # ------------------------------------------------------------------
    # S: NSS shells in series
    # ------------------------------------------------------------------
    if algn == 0:
        Ns = NSS

        if R == 1:
            try:
                Ps = P / (P - Ns * P + Ns)
                Pmax_s = 2.0 / (R + 1.0 + (R**2 + 1.0)**0.5)

                if Pmax_s * Xp > Ps:
                    FNs = (
                        Ps * 2.0**0.5
                    ) / (
                        (1.0 - Ps)
                        * __import__("numpy").log(
                            (2.0 - Ps * (R + 1.0 - (R**2 + 1.0)**0.5))
                            / (2.0 - Ps * (R + 1.0 + (R**2 + 1.0)**0.5))
                        )
                    )
                else:
                    FNs = 0.01
            except Exception:
                FNs = 0.01

        else:
            try:
                Ps = (
                    (((1.0 - P * R) / (1.0 - P)) ** (1.0 / Ns) - 1.0)
                    /
                    (((1.0 - P * R) / (1.0 - P)) ** (1.0 / Ns) - R)
                )

                Pmax_s = 2.0 / (R + 1.0 + (R**2 + 1.0)**0.5)

                if Pmax_s * Xp > Ps:
                    FNs = (
                        (R**2 + 1.0)**0.5
                        * __import__("numpy").log((1.0 - Ps) / (1.0 - R * Ps))
                    ) / (
                        (R - 1.0)
                        * __import__("numpy").log(
                            (2.0 - Ps * (R + 1.0 - (R**2 + 1.0)**0.5))
                            / (2.0 - Ps * (R + 1.0 + (R**2 + 1.0)**0.5))
                        )
                    )
                else:
                    FNs = 0.01
            except Exception:
                FNs = 0.01

        return float(FNs)

    # ------------------------------------------------------------------
    # SP: hot in series, cold in parallel
    # ------------------------------------------------------------------
    if algn == 2:
        Ns = NSS

        R1 = R / Ns
        P1 = Ns / R * (1.0 - (1.0 - P * R) ** (1.0 / Ns))

        # F_1N for the transformed single-shell problem.
        if R1 == 1:
            Pmax_1 = 2.0 / (R1 + 1.0 + (R1**2 + 1.0)**0.5)
            if Pmax_1 * Xp > P1:
                try:
                    F1Nsp = (
                        P1 * 2.0**0.5
                    ) / (
                        (1.0 - P1)
                        * __import__("numpy").log(
                            (2.0 - P1 * (R1 + 1.0 - (R1**2 + 1.0)**0.5))
                            / (2.0 - P1 * (R1 + 1.0 + (R1**2 + 1.0)**0.5))
                        )
                    )
                except Exception:
                    F1Nsp = 0.01
            else:
                F1Nsp = 0.01
        else:
            Pmax_1 = 2.0 / (R1 + 1.0 + (R1**2 + 1.0)**0.5)
            if Pmax_1 * Xp > P1:
                try:
                    F1Nsp = (
                        (R1**2 + 1.0)**0.5
                        * __import__("numpy").log((1.0 - P1) / (1.0 - R1 * P1))
                    ) / (
                        (R1 - 1.0)
                        * __import__("numpy").log(
                            (2.0 - P1 * (R1 + 1.0 - (R1**2 + 1.0)**0.5))
                            / (2.0 - P1 * (R1 + 1.0 + (R1**2 + 1.0)**0.5))
                        )
                    )
                except Exception:
                    F1Nsp = 0.01
            else:
                F1Nsp = 0.01

        try:
            if R != 1 and R1 != 1 and (
                (1.0 - P) / (1.0 - P * R) > 0
            ) and (
                (R - Ns) / (R * (1.0 - P * R)**(1.0 / Ns)) + Ns / R > 0
            ):
                Fsp = (
                    F1Nsp / Ns
                    * ((R - Ns) / (R - 1.0))
                    * (
                        __import__("numpy").log((1.0 - P) / (1.0 - P * R))
                        /
                        __import__("numpy").log(
                            (R - Ns) / (R * (1.0 - P * R)**(1.0 / Ns))
                            + Ns / R
                        )
                    )
                )
            elif R == 1:
                Fsp = (
                    F1Nsp / Ns
                    * (P * (1.0 - Ns) / (1.0 - P))
                    / __import__("numpy").log(
                        (1.0 - Ns) / ((1.0 - P)**(1.0 / Ns)) + Ns
                    )
                )
            elif R1 == 1:
                Fsp = (
                    F1Nsp
                    * (
                        (1.0 - P * Ns)**(1.0 / Ns)
                        / (1.0 - (1.0 - P * Ns)**(1.0 / Ns))
                        / (Ns - 1.0)
                    )
                    * __import__("numpy").log(
                        (1.0 - P) / (1.0 - P * Ns)
                    )
                )
            else:
                Fsp = 0.01
        except Exception:
            Fsp = 0.01

        return float(Fsp)

    # ------------------------------------------------------------------
    # PS: hot in parallel, cold in series
    # ------------------------------------------------------------------
    if algn == 3:
        Ns = NSS

        R1 = R * Ns
        P1 = 1.0 - (1.0 - P) ** (1.0 / Ns)

        Pmax_1 = 2.0 / (R1 + 1.0 + (R1**2 + 1.0)**0.5)

        if Pmax_1 * Xp > P1:
            if R1 == 1:
                aux = (
                    2.0 - P1 * (R1 + 1.0 - (R1**2 + 1.0)**0.5)
                ) / (
                    2.0 - P1 * (R1 + 1.0 + (R1**2 + 1.0)**0.5)
                )

                if aux <= 0:
                    F1Nps = 0.01
                else:
                    try:
                        F1Nps = (
                            P1 * 2.0**0.5
                        ) / (
                            (1.0 - P1)
                            * __import__("numpy").log(aux)
                        )
                    except Exception:
                        F1Nps = 0.01
            else:
                aux1 = (1.0 - P1) / (1.0 - R1 * P1)
                aux2 = (
                    2.0 - P1 * (R1 + 1.0 - (R1**2 + 1.0)**0.5)
                ) / (
                    2.0 - P1 * (R1 + 1.0 + (R1**2 + 1.0)**0.5)
                )

                if aux2 > 1e7:
                    aux2 = -1

                if aux1 > 0 and aux2 > 0:
                    try:
                        F1Nps = (
                            (R1**2 + 1.0)**0.5
                            * __import__("numpy").log(
                                (1.0 - P1) / (1.0 - R1 * P1)
                            )
                        ) / (
                            (R1 - 1.0)
                            * __import__("numpy").log(aux2)
                        )
                    except Exception:
                        F1Nps = 0.01
                else:
                    F1Nps = 0.01
        else:
            F1Nps = 0.01

        try:
            if R != 1 and R1 != 1:
                Fps = (
                    -F1Nps / Ns
                    * ((Ns * R - 1.0) / (R - 1.0))
                    * (
                        __import__("numpy").log((1.0 - P) / (1.0 - P * R))
                        /
                        __import__("numpy").log(
                            (1.0 - Ns * R) / ((1.0 - P)**(1.0 / Ns))
                            + Ns * R
                        )
                    )
                )
            elif R == 1:
                Fps = (
                    F1Nps / Ns
                    * (P * (1.0 - Ns) / (1.0 - P))
                    / __import__("numpy").log(
                        (1.0 - Ns) / ((1.0 - P)**(1.0 / Ns)) + Ns
                    )
                )
            elif R1 == 1:
                Fps = (
                    -F1Nps
                    * (
                        (1.0 - P)**(1.0 / Ns)
                        / (1.0 - (1.0 - P)**(1.0 / Ns))
                        / (Ns - 1.0)
                    )
                    * __import__("numpy").log(
                        (1.0 - P) / (1.0 - P / Ns)
                    )
                )
            else:
                Fps = 0.01
        except Exception:
            Fps = 0.01

        return float(Fps)

    raise ValueError(
        f"Invalid algn value: {algn}. Expected 0 (S), 1 (P), 2 (SP), or 3 (PS)."
    )


def Areq(Ds, dte, Npt, rp, lay, L, Nb, Bc, NSS, algn, m_p):
    # Required area constraint
    print(">>> Areq", NSS, algn)
    Q = Calculations_HEX_heatload.HEX_heat_load(
        m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho']
    )

    # Calculate the flow rates through one STHE unit according to
    # the selected multi-STHE configuration.
    mt_unit = _tube_mass_flowrate(m_p, NSS, algn)
    ms_unit = _shell_mass_flowrate(m_p, NSS, algn)

    # U is calculated for one STHE unit. The multi-STHE configuration
    # affects U only through the flow rate seen by that unit.
    U = Calculations_STHE_U.STHE_overall_coefficient(
        mt_unit, m_p['rot'], m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'],
        ms_unit, m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
        m_p['thk'], m_p['ktube'], m_p['yfluid'], Ds, dte, Npt, rp, lay, L,
        Nb, Bc, m_p
    )

    LMTD = Calculations_HEX_LMTD.HEX_lmtd(
        m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco']
    )

    # Global LMTD correction factor for the complete multi-STHE
    # configuration.
    F = _F_total(
        m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'],
        Npt, NSS, algn, m_p['Xp']
    )

    A = Calculations_STHE_area.STHE_area(
        Ds, dte, Npt, rp, lay, L, m_p
    )

    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - A
    return fun_val

def TAC_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Objective function
    TAC = Calculations_STHE_TAC.STHE_TAC(m_p['int_rate'], m_p['n'], m_p['par_a'], m_p['par_b'], m_p['Nop'], m_p['pc'],
                                         m_p['eta'], Ds, dte, Npt, rp, lay, L, m_p['ms'], m_p['mt'], m_p['ros'],
                                         m_p['rot'], m_p['mis'], m_p['mit'], m_p['thk'], Nb, Bc, m_p)
    return TAC

def AREA_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Area = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    return Area
    
def CAPEX_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    CAPEX = Calculations_STHE_CAPEX.STHE_CAPEX(m_p['par_a'], m_p['par_b'], Ds, dte, Npt, rp, lay, L, m_p)
    return CAPEX

# endregion
##################################################################################################################
