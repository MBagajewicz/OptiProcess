###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          19-Mar-2025     Mariana Mello             Add constraints
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
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
from GPHE.Calculations import (
    Calculations_GPHE_velocity,
    Calculations_GPHE_DeltaP_channel,
    Calculations_GPHE_DeltaP_port,
    Calculations_GPHE_U,
    Calculations_GPHE_epsilon_Nutcalc,
    Calculations_GPHE_correction_factor,
    Calculations_GPHE_Reynolds,
    Calculations_GPHE_area
)
from WC_GPHE.Calculations import Calculations_WC_GPHE_flowrates, Calculations_WC_GPHE_TAC
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
import numpy as np
from scipy import optimize
# endregion
##################################################################################################################

# -------------------------------------------------------------------------------------------------------------------
#  Regular Set Trimming Functions
# -------------------------------------------------------------------------------------------------------------------

def vh_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on vh
    Lw = m_p['ppLw'][Pl]
    vh = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Nph, m_p['bp'], m_p['mh'], m_p['roc'])
    fun_val = m_p['vhmin'] - vh
    return fun_val

def vh_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on vh
    Lw = m_p['ppLw'][Pl]
    vh = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Nph, m_p['bp'], m_p['mh'], m_p['roc'])
    fun_val = vh - m_p['vhmax']
    return fun_val

def Reh_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on Ret
    Lw = m_p['ppLw'][Pl]
    Reh = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Nph, m_p['bp'], m_p['phi'], m_p['roh'], m_p['mih'], m_p['mh'])
    fun_val = Reh - m_p['Rehmax']
    return fun_val

def Reh_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on Reh
    Lw = m_p['ppLw'][Pl]
    Reh = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Nph, m_p['bp'], m_p['phi'], m_p['roh'], m_p['mih'], m_p['mh'])
    fun_val = m_p['Rehmin'] - Reh
    return fun_val

def DPh_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on DPt
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    DPh_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Nph, Sa, m_p['bp'], m_p['phi'],
                                                                 m_p['roh'], m_p['mih'], m_p['mh'])
    DPh_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, m_p['mh'], m_p['roh'])
    DPh = DPh_c + DPh_p
    #print('DPh',DPh)
    fun_val = DPh - m_p['DPhdisp']
    return fun_val

# -------------------------------------------------------------------------------------------------------------------
#  Proxy Set Trimming Functions
# -------------------------------------------------------------------------------------------------------------------

def vc_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on vt
    # Calculate Fw_PST_min
    Lw = m_p['ppLw'][Pl]
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'], m_p['Recmin'])
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])
    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), Fw_fixed)

    # Calculate the velocity with Fw_PST_min
    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, m_p['bp'], Fw_PST_min, m_p['roc'])

    fun_val = vc - m_p['vcmax']
    return fun_val

def vc_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on vt
    # Calculate Fw_PST_max
    Lw = m_p['ppLw'][Pl]
    Fw_vel_max = Calculations_WC_GPHE_flowrates.WC_Fw_vel_max(Ntp, Npc, m_p['bp'], Lw, m_p['vcmax'], m_p['roc'])
    Fw_Re_max = Calculations_WC_GPHE_flowrates.WC_Fw_Re_max(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'], m_p['Recmax'])
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])
    # Calculate the velocity with Fw_PST_max
    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, m_p['bp'], Fw_PST_max, m_p['roc'])

    fun_val = m_p['vcmin'] - vc
    return fun_val

def Rec_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on Rec
    Lw = m_p['ppLw'][Pl]
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'], m_p['Recmin'])

    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])
    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), Fw_fixed)

    Rec = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Npc, m_p['bp'], m_p['phi'], m_p['roc'], m_p['mic'], Fw_PST_min)
    fun_val = Rec - m_p['Recmax']
    return fun_val

def Rec_lb(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound on Rec
    Lw = m_p['ppLw'][Pl]
    # Calculate Fw_PST_max
    Fw_vel_max = Calculations_WC_GPHE_flowrates.WC_Fw_vel_max(Ntp, Npc, m_p['bp'], Lw, m_p['vcmax'], m_p['roc'])
    Fw_Re_max = Calculations_WC_GPHE_flowrates.WC_Fw_Re_max(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'], m_p['Recmax'])
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Rec = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Npc, m_p['bp'], m_p['phi'], m_p['roc'], m_p['mic'], Fw_PST_max)
    fun_val = m_p['Recmin'] - Rec
    return fun_val

def Tco_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    Lw = m_p['ppLw'][Pl]
    Fw_vel_max = Calculations_WC_GPHE_flowrates.WC_Fw_vel_max(Ntp, Npc, m_p['bp'], Lw, m_p['vcmax'], m_p['roc'])
    Fw_Re_max = Calculations_WC_GPHE_flowrates.WC_Fw_Re_max(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'], m_p['Recmax'])
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    Tco = Q/(m_p['Cpc']*Fw_PST_max) + m_p['Tci']
    Tco_deltaTmin = m_p['Tho'] - m_p['DeltaT_min']
    m_p['Tco_min'] = min(m_p['Tco_max'], Tco_deltaTmin)
    fun_val = Tco - m_p['Tco_min']
    return fun_val

def Areq(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Required area constraint
    Lw = m_p['ppLw'][Pl]
    Lp = m_p['ppLp'][Pl]
    Fw_vel_max = Calculations_WC_GPHE_flowrates.WC_Fw_vel_max(Ntp, Npc, m_p['bp'], Lw, m_p['vcmax'], m_p['roc'])
    Fw_Re_max = Calculations_WC_GPHE_flowrates.WC_Fw_Re_max(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmax'])
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    Tco = Q/(m_p['Cpc']*Fw_PST_max) + m_p['Tci']
    U = Calculations_GPHE_U.GPHE_overall_coefficient(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                     m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                     m_p['mic'],  m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                     m_p['roh'], Fw_PST_max, m_p['mh'])
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco)
    #xo = np.array([1, 0.8, 0.9])
    tam = len(Fw_PST_max)
    xo = np.ones((3, tam))
    solutions = []
    for i in range(tam):
        x0_set = xo[:, i]
        Fw_PST_max_i = Fw_PST_max[i]

        sol = optimize.root(Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc, x0_set,
                            args=(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'], m_p['Tci'], Fw_PST_max_i, m_p['Cpc']))
        solutions.append(sol.x)
    solutions = np.array(solutions).T
    F1_2 = (m_p['Thi'] - m_p['Tho']) / LMTD / solutions[0, :]
    F = Calculations_GPHE_correction_factor.GPHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco, Nph, Npc,
                                                                   F1_2)
    #print('F',F)
    NTP_termicos = Ntp - 2
    Atermica = Calculations_GPHE_area.GPHE_area(m_p['phi'], NTP_termicos, Lp, Lw)
    #print('Area', Atermica)
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - Atermica
    return fun_val

def DPc_ub(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on DPc
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])
    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), Fw_fixed)

    DPc_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Npc, Sa, m_p['bp'], m_p['phi'],
                                                                 m_p['roc'], m_p['mic'], Fw_PST_min)
    DPc_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, Fw_PST_min, m_p['roc'])
    DPc = DPc_c + DPc_p

    fun_val = DPc - m_p['DPcdisp']
    return fun_val

# endregion

######################################################################################################################

# region LB function

# -------------------------------------------------------------------------------------------------------------------
# Lower Bound Function
# --------------------------------------------------------------------------------------------------------------------

def LB_WC_GPHE(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Lower bound using the value of the minimum water flowrate used for Proxy Set Trimming
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])
    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), Fw_fixed)

    LB = Calculations_WC_GPHE_TAC.WC_GPHE_TAC(Fw_PST_min, Ntp, Lp, Lw, Dp, Npc, Sa, m_p['bp'], m_p['phi'], m_p['roc'],
                                              m_p['mic'], m_p['pcw'], m_p['pc'], m_p['eta'], m_p['Nop'], m_p['cf'],
                                              m_p['cv'], m_p['alpha'], m_p['int_rate'], m_p['n'], Nph, m_p['mh'],
                                              m_p['roh'], m_p['mih'])
    return LB

# endregion

######################################################################################################################
# region OF function

# --------------------------------------------------------------------------------------------------------------------
# Objective Function
# --------------------------------------------------------------------------------------------------------------------

def TAC_OF(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Objective function
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_hat = Calculations_WC_GPHE_flowrates.WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                      m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                      m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                      m_p['roh'], m_p['mh'], m_p['Thi'], m_p['Tho'], m_p['Tci'],
                                                      m_p['Aexc'], m_p['vcmin'], m_p['Recmin'], m_p['Fw_Thi_min'],
                                                      m_p['Fw_Tco_min'], m_p['vcmax'], m_p['Recmax'], m_p['Fw_max'])
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), m_p['Fw_Tco_min'])
    #print('Fw_water', Fw_min)

    OF_Solution = Calculations_WC_GPHE_TAC.WC_GPHE_TAC(Fw_min, Ntp, Lp, Lw, Dp, Npc, Sa, m_p['bp'], m_p['phi'], m_p['roc'],
                                                       m_p['mic'], m_p['pcw'], m_p['pc'], m_p['eta'], m_p['Nop'], m_p['cf'],
                                                       m_p['cv'], m_p['alpha'], m_p['int_rate'], m_p['n'], Nph,
                                                       m_p['mh'], m_p['roh'], m_p['mih'])
    return OF_Solution

# endregion

#######################################################################################################################
# region Smart Enumeration Constraints

# -------------------------------------------------------------------------------------------------------------------
# Smart Enumeration Functions
# -------------------------------------------------------------------------------------------------------------------

def Fw_ub_SE(Ntp, Pl, Sa, Nph, Npc, m_p):
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_hat = Calculations_WC_GPHE_flowrates.WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                      m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                      m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                      m_p['roh'], m_p['mh'], m_p['Thi'], m_p['Tho'], m_p['Tci'],
                                                      m_p['Aexc'], m_p['vcmin'],
                                                      m_p['Recmin'], m_p['Fw_Thi_min'], m_p['Fw_Tco_min'],
                                                      m_p['vcmax'], m_p['Recmax'], m_p['Fw_max'])
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), m_p['Fw_Tco_min'])

    fun_val_SE = Fw_min - m_p['Fw_max']
    return fun_val_SE

def vc_ub_SE(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on vt
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_hat = Calculations_WC_GPHE_flowrates.WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                      m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                      m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                      m_p['roh'], m_p['mh'], m_p['Thi'], m_p['Tho'], m_p['Tci'],
                                                      m_p['Aexc'], m_p['vcmin'],
                                                      m_p['Recmin'], m_p['Fw_Thi_min'], m_p['Fw_Tco_min'],
                                                      m_p['vcmax'], m_p['Recmax'], m_p['Fw_max'])
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), m_p['Fw_Tco_min'])

    vc = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Npc, m_p['bp'], Fw_min, m_p['roc'])

    fun_val_SE = vc - m_p['vcmax']

    return fun_val_SE

def Rec_ub_SE(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on Rec
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_hat = Calculations_WC_GPHE_flowrates.WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                      m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                      m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                      m_p['roh'], m_p['mh'], m_p['Thi'], m_p['Tho'], m_p['Tci'],
                                                      m_p['Aexc'], m_p['vcmin'],
                                                      m_p['Recmin'], m_p['Fw_Thi_min'], m_p['Fw_Tco_min'],
                                                      m_p['vcmax'], m_p['Recmax'], m_p['Fw_max'])
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), m_p['Fw_Tco_min'])

    Rec = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Npc, m_p['bp'], m_p['phi'], m_p['roc'], m_p['mic'], Fw_min)

    fun_val_SE = Rec - m_p['Recmax']
    return fun_val_SE


def DPc_ub_SE(Ntp, Pl, Sa, Nph, Npc, m_p):
    # Upper bound on DPt
    Lp = m_p['ppLp'][Pl]
    Lw = m_p['ppLw'][Pl]
    Dp = m_p['ppDp'][Pl]
    Fw_hat = Calculations_WC_GPHE_flowrates.WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, m_p['Rfh'], m_p['Rfc'], m_p['thk'],
                                                      m_p['kplate'], m_p['bp'], m_p['phi'], m_p['Cpc'], m_p['Cph'],
                                                      m_p['mic'], m_p['mih'], m_p['kc'], m_p['kh'], m_p['roc'],
                                                      m_p['roh'], m_p['mh'], m_p['Thi'], m_p['Tho'], m_p['Tci'],
                                                      m_p['Aexc'], m_p['vcmin'],
                                                      m_p['Recmin'], m_p['Fw_Thi_min'], m_p['Fw_Tco_min'],
                                                      m_p['vcmax'], m_p['Recmax'], m_p['Fw_max'])
    Fw_vel_min = Calculations_WC_GPHE_flowrates.WC_Fw_vel_min(Ntp, Npc, m_p['bp'], Lw, m_p['vcmin'], m_p['roc'])
    Fw_Re_min = Calculations_WC_GPHE_flowrates.WC_Fw_Re_min(Ntp, Npc, m_p['bp'], m_p['phi'], Lw, m_p['mic'],
                                                            m_p['Recmin'])
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), m_p['Fw_Tco_min'])

    DPc_c = Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Npc, Sa, m_p['bp'], m_p['phi'],
                                                                 m_p['roc'], m_p['mic'], Fw_min)
    DPc_p = Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, Fw_min, m_p['roc'])
    DPc = DPc_c + DPc_p
    #print('Dpc',DPc)

    fun_val_SE = DPc - m_p['DPcdisp']
    return fun_val_SE
