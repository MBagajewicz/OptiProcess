###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          01-Dec-2024     Mariana Mello             Add constraints
#   0.3          28-Feb-2025     Alice Peccini             Relocating folders 
#   0.4          07-Jun-2025     Qiqi Zhang                Adaptation from original STHE
###################################################################################################################
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
from SPHE_LMTD.Calculations import (
    Calculations_SPHE_LMTD_Reynolds,
    Calculations_SPHE_LMTD_velocity,
    Calculations_SPHE_LMTD_correction_factor,
    Calculations_SPHE_LMTD_area,
    Calculations_SPHE_LMTD_TAC,
    Calculations_SPHE_LMTD_DeltaP,
    Calculations_SPHE_LMTD_U
)
from Common_Equations_HEX import Calculations_HEX_LMTD, Calculations_HEX_heatload
# endregion
##################################################################################################################

##################################################################################################################
# region Example 1

def LH_lb(L, H, ds, dh, dc,m_p):
    # Lower bound on L/H
    fun_val = m_p['LBLH'] - L / H
    return fun_val

def LH_ub(L, H, ds, dh, dc, m_p):
    # Upper bound on L/H
    fun_val = L / H - m_p['UBLH']
    return fun_val

def vh_lb(L, H, ds, dh, dc, m_p):
    # Lower bound on vh
    vh, _ = Calculations_SPHE_LMTD_velocity.SPHE_velocity(m_p['mh'], m_p['mc'], H, dh, dc, m_p['roh'], m_p['roc'])
    fun_val = m_p['vhmin'] - vh
    return fun_val

def vh_ub(L, H, ds, dh, dc, m_p):
    # Upper bound on vh
    vh, _ = Calculations_SPHE_LMTD_velocity.SPHE_velocity(m_p['mh'], m_p['mc'], H, dh, dc, m_p['roh'], m_p['roc'])
    fun_val = vh - m_p['vhmax']
    return fun_val

def vc_lb(L, H, ds, dh, dc, m_p):
    # Lower bound on vt
    _, vc = Calculations_SPHE_LMTD_velocity.SPHE_velocity(m_p['mh'], m_p['mc'], H, dh, dc, m_p['roh'], m_p['roc'])
    fun_val = m_p['vcmin'] - vc
    return fun_val

def vc_ub(L, H, ds, dh, dc, m_p):
    # Upper bound on vt
    _, vc = Calculations_SPHE_LMTD_velocity.SPHE_velocity(m_p['mh'], m_p['mc'], H, dh, dc, m_p['roh'], m_p['roc'])
    fun_val = vc - m_p['vcmax']
    return fun_val

def Reh_lb(L, H, ds, dh, dc,m_p):
    # Lower bound on Reh
    _, _, Reeh, _ = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, m_p['mh'], m_p['mc'], m_p['mih'], m_p['mic'], L, m_p['thk'], ds)
    Reh, _, _, _ = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, m_p['mh'], m_p['mc'], m_p['mih'], m_p['mic'], L, m_p['thk'], ds)
    fun_val = Reeh - Reh
    return fun_val

def Rec_lb(L, H, ds, dh, dc, m_p):
    # Lower bound on Rec
    _, _, _, Reec = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, m_p['mh'], m_p['mc'], m_p['mih'], m_p['mic'], L, m_p['thk'], ds)
    _, Rec, _, _ = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, m_p['mh'], m_p['mc'], m_p['mih'], m_p['mic'], L, m_p['thk'], ds)
    fun_val = Reec - Rec
    return fun_val

def dltph_ub(L, H, ds, dh, dc, m_p):
    # Upper bound on dltph
    dltph, _ = Calculations_SPHE_LMTD_DeltaP.SPHE_DeltaP(L, m_p['roh'], m_p['roc'], m_p['mh'], m_p['mc'], H, dh, dc, m_p['mih'], m_p['mic'])
    fun_val = dltph - m_p['DPhdisp']
    return fun_val

def dltpc_ub(L, H, ds, dh, dc, m_p):
    # Upper bound on dltpc
    _, dltpc = Calculations_SPHE_LMTD_DeltaP.SPHE_DeltaP(L, m_p['roh'], m_p['roc'], m_p['mh'], m_p['mc'], H, dh, dc, m_p['mih'], m_p['mic'])
    fun_val = dltpc - m_p['DPcdisp']
    return fun_val

def Areq(L, H, ds, dh, dc, m_p):
    # Required area constraint
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    U = Calculations_SPHE_LMTD_U.SPHE_overall_coefficient(L, dh, dc, ds, H, m_p['thk'], m_p['mh'], m_p['mc'], m_p['mih'],
                                                     m_p['mic'], m_p['Cph'], m_p['Cpc'], m_p['kh'], m_p['kc'], m_p['Rfh'],
                                                     m_p['Rfc'], m_p['kplate'])
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'])
    F = Calculations_SPHE_LMTD_correction_factor.SPHE_correction_factor(L, H, dh, dc, ds, m_p['thk'], m_p['mh'], m_p['mc'],
                                                                   m_p['mih'], m_p['mic'], m_p['Cph'], m_p['Cpc'], m_p['kh'],
                                                                   m_p['kc'], m_p['Rfh'], m_p['Rfc'], m_p['kplate'])
    A = Calculations_SPHE_LMTD_area.SPHE_area(L, H)
    Areq = (Q * 3.412152) / (U*1.8 * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - A/(0.3048**2)
    return fun_val

def SPHE_OF(L, H, ds, dh, dc, m_p):
    # Objective function
    OF_Solution = Calculations_SPHE_LMTD_TAC.SPHE_TAC(m_p['int_rate'], m_p['n'], m_p['par_a'], m_p['par_b'], H, L, m_p['pc'],
                                                 m_p['eta'], m_p['mh'], m_p['mc'], m_p['roh'], m_p['roc'], dh, dc, m_p['mih'],
                                                 m_p['mic'], m_p['Nop'])
    return OF_Solution

# endregion
##################################################################################################################

