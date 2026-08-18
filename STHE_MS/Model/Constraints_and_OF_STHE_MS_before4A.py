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
# endregion
##################################################################################################################

##################################################################################################################
# region Constraints


def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on L/Ds
    fun_val = m_p['LBLD'] - L / Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on L/Ds
    fun_val = L / Ds - m_p['UBLD']
    return fun_val
def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = 0.2 * Ds - lbc
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = lbc - 1 * Ds
    return fun_val

def lbmax(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    lbc = (L / (Nb + 1))
    if m_p['Shell_Method'] == 'Bell':
        lbmax = (m_p['plbmax1']*dte + m_p['plbmax2'])*0.5
    elif m_p['Shell_Method'] == 'Kern':
        lbmax = lbc*1e10
    fun_val = lbc - lbmax
    return fun_val

def _shell_mass_flowrate(m_p, NSS, algn):
    """
    Return the mass flow rate through one shell for the selected
    multi-shell structure.

    algn = 0 -> S  : shell flow remains in series
    algn = 1 -> P  : shell flow is split among NSS shells
    algn = 2 -> SP : hot stream in series, cold stream in parallel
    algn = 3 -> PS : cold stream in series, hot stream in parallel
    """
    if NSS < 1:
        raise ValueError("NSS must be greater than or equal to 1.")

    yfluid = m_p['yfluid']

    if algn == 0:
        shell_is_parallel = False
    elif algn == 1:
        shell_is_parallel = True
    elif algn == 2:
        # SP: hot in series, cold in parallel.
        shell_is_parallel = (yfluid == 'hot_stream')
    elif algn == 3:
        # PS: cold in series, hot in parallel.
        shell_is_parallel = (yfluid == 'cold_stream')
    else:
        raise ValueError(
            f"Invalid algn value: {algn}. Expected 0, 1, 2, or 3."
        )

    return m_p['ms'] / NSS if shell_is_parallel else m_p['ms']


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
    """
    Return the mass flow rate through one shell's tube side.

    algn = 0 -> S  : tube flow remains in series
    algn = 1 -> P  : tube flow is split among NSS shells
    algn = 2 -> SP : hot stream in series, cold stream in parallel
    algn = 3 -> PS : cold stream in series, hot stream in parallel

    The tube-side flow is therefore split for:
        P  -> always
        SP -> when cold_stream is in the tubes
        PS -> when hot_stream is in the tubes
    """
    if NSS < 1:
        raise ValueError("NSS must be greater than or equal to 1.")

    yfluid = m_p['yfluid']

    if algn == 0:
        tube_is_parallel = False
    elif algn == 1:
        tube_is_parallel = True
    elif algn == 2:
        # SP: hot in series, cold in parallel.
        tube_is_parallel = (yfluid == 'cold_stream')
    elif algn == 3:
        # PS: cold in series, hot in parallel.
        tube_is_parallel = (yfluid == 'hot_stream')
    else:
        raise ValueError(
            f"Invalid algn value: {algn}. Expected 0, 1, 2, or 3."
        )

    return m_p['mt'] / NSS if tube_is_parallel else m_p['mt']


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
    """
    Return the number of shells crossed in series by the shell-side stream.

    This reproduces the series-selection logic used by the original
    ApproachSelection.DPs_func without introducing the Flet-only Nps variable.
    """
    if NSS < 1:
        raise ValueError("NSS must be greater than or equal to 1.")

    yfluid = m_p['yfluid']

    if algn == 0:
        return NSS
    if algn == 1:
        return 1
    if algn == 2:
        # SP: hot in series, cold in parallel.
        # Shell is cold when hot is in the tubes.
        return NSS if yfluid == 'hot_stream' else 1
    if algn == 3:
        # PS: cold in series, hot in parallel.
        # Shell is hot when cold is in the tubes.
        return NSS if yfluid == 'cold_stream' else 1

    raise ValueError(
        f"Invalid algn value: {algn}. Expected 0, 1, 2, or 3."
    )


def _tube_series_count(m_p, NSS, algn):
    """
    Return the number of shells crossed in series by the tube-side stream.

    This reproduces the series-selection logic used by the original
    ApproachSelection.Dpt_func without introducing the Flet-only Nps variable.
    """
    if NSS < 1:
        raise ValueError("NSS must be greater than or equal to 1.")

    yfluid = m_p['yfluid']

    if algn == 0:
        return NSS
    if algn == 1:
        return 1
    if algn == 2:
        # SP: hot in series, cold in parallel.
        # Tube side is hot when hot_stream is in the tubes.
        return NSS if yfluid == 'hot_stream' else 1
    if algn == 3:
        # PS: cold in series, hot in parallel.
        # Tube side is cold when cold_stream is in the tubes.
        return NSS if yfluid == 'cold_stream' else 1

    raise ValueError(
        f"Invalid algn value: {algn}. Expected 0, 1, 2, or 3."
    )


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

def F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt,
                                                                   m_p['Xp'])
    fun_val = m_p['F_min'] - F
    return fun_val

def Areq(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Required area constraint
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    U = Calculations_STHE_U.STHE_overall_coefficient(m_p['mt'], m_p['rot'], m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'],
                                                     m_p['ms'], m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                     m_p['thk'], m_p['ktube'], m_p['yfluid'], Ds, dte, Npt, rp, lay, L,
                                                     Nb, Bc, m_p)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'])
    #print('LMTD',LMTD)
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt,
                                                                   m_p['Xp'])
    #print('F',F)
    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    #print('A',A)
    Areq = Q / (U * LMTD * F)
    #print('Areq',Areq)
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
