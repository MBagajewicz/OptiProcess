###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          01-Dec-2024     Mariana Mello             Add constraints Example 1
#   0.3          28-Feb-2025     Alice Peccini             Relocating folders
#   0.4          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
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
import numpy as np
from scipy import optimize
from GPHE.Calculations import (
    Calculations_GPHE_velocity,
    Calculations_GPHE_DeltaP_channel,
    Calculations_GPHE_DeltaP_port,
    Calculations_GPHE_U,
    Calculations_GPHE_epsilon_Nutcalc,
    Calculations_GPHE_correction_factor,
    Calculations_GPHE_area,
    Calculations_GPHE_CAPEX,
    Calculations_GPHE_TAC
)
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
# endregion
##################################################################################################################

##################################################################################################################
# region calculations

def vh_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    # Lower bound on vh
    vh = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Nph, m_p['bp'], m_p['mh'], m_p['roh'])
    fun_val = m_p['vhmin'] - vh
    return fun_val

def vh_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on vh
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    vh = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Nph, m_p['bp'], m_p['mh'], m_p['roh'])
    fun_val = vh - m_p['vhmax']
    return fun_val

def vc_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on vc
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, m_p['bp'], m_p['mc'], m_p['roc'])
    fun_val = m_p['vcmin'] - vc
    return fun_val

def vc_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on vc
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, m_p['bp'], m_p['mc'], m_p['roc'])
    fun_val = vc - m_p['vcmax']
    return fun_val

def DPh_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on DPh
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    DPh_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Nph, Sa, m_p['bp'], m_p['phi'],
                                                                 m_p['roh'], m_p['mih'], m_p['mh'])
    DPh_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, m_p['mh'], m_p['roh'])
    DPh_t = DPh_c + DPh_p
    fun_val = DPh_t - m_p['DPhdisp']
    return fun_val

def DPc_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on DPc
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    DPc_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Npc, Sa, m_p['bp'], m_p['phi'],
                                                                 m_p['roc'], m_p['mic'], m_p['mc'])
    DPc_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, m_p['mc'], m_p['roc'])
    DPc_t = DPc_c + DPc_p
    fun_val = DPc_t - m_p['DPcdisp']
    return fun_val

def Areq(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Required area constraint
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    U = Calculations_GPHE_U.GPHE_overall_coefficient(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                     m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                     m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                     m_p['roh'], m_p['mc'], m_p['mh'])
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'])
    xo = np.array([1, 0.8, 0.9])
    xsol = optimize.root(Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc, xo, args=(m_p['mh'], m_p['Cph'],
                                                                                           m_p['Thi'], m_p['Tho'],
                                                                                           m_p['Tci'], m_p['mc'],
                                                                                           m_p['Cpc']))
    F1_2 = (m_p['Thi'] - m_p['Tho']) / LMTD / xsol.x[0]
    F = Calculations_GPHE_correction_factor.GPHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Nph,
                                                                   Npc, F1_2)
    NTP_termicos = Ntp - 2
    Atermica = (Calculations_GPHE_area.GPHE_area(m_p['phi'], NTP_termicos, Lp, Lw))
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - Atermica
    return fun_val

# --------------------------------------------------------------------------------------------------------------------
# Objective Function
# --------------------------------------------------------------------------------------------------------------------

def TAC_OF(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Objective function
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    TAC = Calculations_GPHE_TAC.GPHE_TAC(m_p['int_rate'], m_p['n'], Ntp, Lp, Lw, m_p['par_a'], m_p['par_b'], Dp, Nph,
                                         Npc, Sa, m_p['Nop'], m_p['pc'], m_p['eta'], m_p['phi'], m_p['bp'], m_p['mh'],
                                         m_p['mc'], m_p['roh'], m_p['roc'], m_p['mih'], m_p['mic'])
    return TAC

def AREA_OF(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Objective function
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Area = Calculations_GPHE_area.GPHE_area(m_p['phi'], Ntp, Lp, Lw)
    return Area

def CAPEX_OF(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Objective function
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    CAPEX = Calculations_GPHE_CAPEX.GPHE_CAPEX(Ntp, Lp, Lw, m_p['par_a'], m_p['par_b'], m_p['phi'])
    return CAPEX

# endregion
##################################################################################################################
