###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          01-Dec-2024     Mariana Mello             Add constraints
#   0.3          23-Apr-2025     Mariana Mello             Update to fix error and add constraint Fmin
#   0.4          06-May-2025     Mariana Mello             Revision from paper
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
##################################################################################################################

##################################################################################################################
# region Import Library
from STHE.Calculations import (
    Calculations_STHE_DeltaPtubeside,
    Calculations_STHE_DeltaPshellside,
    Calculations_STHE_U,
    Calculations_STHE_correction_factor,
    Calculations_STHE_area,
    Calculations_STHE_velocity_tubeside,
    Calculations_STHE_velocity_shellside,
    Calculations_STHE_Reynolds_tubeside,
    Calculations_STHE_Reynolds_shellside,
    Calculations_STHE_htubeside)
from WC_STHE.Calculations import (
    Calculations_WC_STHE_flowrates,
    Calculations_WC_STHE_TAC)
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
from STHE.Model import Constraints_and_OF_STHE
import numpy as np
# endregion
##################################################################################################################
##################################################################################################################

# region Set Trimming Constraints

# -------------------------------------------------------------------------------------------------------------------
#  Regular Set Trimming Functions
# -------------------------------------------------------------------------------------------------------------------

def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on L/Ds
    fun_val = Constraints_and_OF_STHE.LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on L/Ds
    fun_val = Constraints_and_OF_STHE.LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on lbc
    fun_val = Constraints_and_OF_STHE.lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on lbc
    fun_val = Constraints_and_OF_STHE.lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vs
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(m_p['ms'], m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p)
    fun_val = m_p['vsmin'] - vs
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vs
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(m_p['ms'], m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p)
    #print('vs',vs)
    fun_val = vs - m_p['vsmax']
    return fun_val

def Res_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Ret
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, rp,
                                                                       lay, L, Nb, m_p)
    #print('Res',Res)
    fun_val = Res - m_p['Resmax']
    return fun_val

def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Ret
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, rp,
                                                                       lay, L, Nb, m_p)
    fun_val = m_p['Resmin'] - Res
    return fun_val

def DPs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on DPt
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, Npt, rp,
                                                                  lay, L, Nb, Bc, m_p)
    #print('DPs',DPs)
    fun_val = DPs - m_p['DPsdisp']
    return fun_val

# -------------------------------------------------------------------------------------------------------------------
#  Proxy Set Trimming Functions
# -------------------------------------------------------------------------------------------------------------------

def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vt
    # Calculate Fw_PST_max
    Fw_vel_max = Calculations_WC_STHE_flowrates.WC_Fw_vel_max(m_p['vtmax'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    #print('Fw_vel_max', Fw_vel_max)
    Fw_Re_max = Calculations_WC_STHE_flowrates.WC_Fw_Re_max(m_p['Retmax'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    #print('Fw_Re_max', Fw_Re_max)
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])
    #print('Fw_PST_max',Fw_PST_max)

    # Calculate the velocity with Fw_PST_max
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(Fw_PST_max, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p)
    #print('vt',vt)
    fun_val = m_p['vtmin'] - vt
    return fun_val

def vt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vt
    # Calculate Fw_PST_min
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    #print('Fw_vel_min',Fw_vel_min)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    #print('Fw_Re_min', Fw_Re_min)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)
    #print('Fw_pass_min',Fw_pass_min)
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])
    #print('Fw_Thi_min', m_p['Fw_Thi_min'])
    #print('Fw_Tco_min', m_p['Fw_Tco_min'])
    #print('Fw_pass_min', m_p['Fw_pass_min'])
    #print('Fw_fixed', Fw_fixed)

    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), np.maximum(Fw_fixed, Fw_pass_min))
    #print('Fw_PST_min', Fw_PST_min)

    # Calculate the velocity with Fw_PST_min
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(Fw_PST_min, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p)
    fun_val = vt - m_p['vtmax']
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Ret
    # Calculate Fw_PST_max
    Fw_vel_max = Calculations_WC_STHE_flowrates.WC_Fw_vel_max(m_p['vtmax'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_max = Calculations_WC_STHE_flowrates.WC_Fw_Re_max(m_p['Retmax'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)

    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(Fw_PST_max, m_p['rot'], m_p['mit'], m_p['thk'], Ds,
                                                                     dte, Npt, rp, lay, m_p)
    fun_val = m_p['Retmin'] - Ret
    return fun_val

def Ret_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on Ret
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])

    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), np.maximum(Fw_fixed, Fw_pass_min))

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(Fw_PST_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds,
                                                                     dte, Npt, rp, lay, m_p)
    fun_val = Ret - m_p['Retmax']
    return fun_val

def Tco_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Fw_vel_max = Calculations_WC_STHE_flowrates.WC_Fw_vel_max(m_p['vtmax'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    #print(Fw_vel_max)
    Fw_Re_max = Calculations_WC_STHE_flowrates.WC_Fw_Re_max(m_p['Retmax'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    Tco = Q/(m_p['Cpc']*Fw_PST_max) + m_p['Tci']
    Tco_deltaTmin = m_p['Tho'] - m_p['DeltaT_min']
    m_p['Tco_min'] = min(m_p['Tco_max'], Tco_deltaTmin)
    #print('Tco_min',m_p['Tco_min'])
    fun_val = Tco - m_p['Tco_min']
    return fun_val

def F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Fw_vel_max = Calculations_WC_STHE_flowrates.WC_Fw_vel_max(m_p['vtmax'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_max = Calculations_WC_STHE_flowrates.WC_Fw_Re_max(m_p['Retmax'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    Tco = Q/(m_p['Cpc']*Fw_PST_max) + m_p['Tci']
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco, Npt, m_p['Xp'])
    fun_val = m_p['F_min'] - F
    return fun_val

def Areq(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Required area constraint
    Fw_vel_max = Calculations_WC_STHE_flowrates.WC_Fw_vel_max(m_p['vtmax'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_max = Calculations_WC_STHE_flowrates.WC_Fw_Re_max(m_p['Retmax'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_PST_max = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), m_p['Fw_max'])

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    Tco = Q/(m_p['Cpc']*Fw_PST_max) + m_p['Tci']
    U = Calculations_STHE_U.STHE_overall_coefficient(Fw_PST_max, m_p['rot'], m_p['Cpt'], m_p['mit'], m_p['kt'],
                                                     m_p['Rft'], m_p['ms'], m_p['ros'], m_p['Cps'], m_p['mis'],
                                                     m_p['ks'], m_p['Rfs'], m_p['thk'], m_p['ktube'], m_p['yfluid'], Ds,
                                                     dte, Npt, rp, lay, L, Nb, Bc, m_p)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco)
    #print('LMTD',LMTD)
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco, Npt, m_p['Xp'])
    #print('F',F)
    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    #print('A',A)
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - A
    return fun_val

def DPt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on DPt
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])

    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), np.maximum(Fw_fixed, Fw_pass_min))

    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(Fw_PST_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte,
                                                                Npt, rp, lay, L, m_p)

    fun_val = DPt - m_p['DPtdisp']
    return fun_val

# endregion

######################################################################################################################

# region LB function

# -------------------------------------------------------------------------------------------------------------------
# Lower Bound Function
# --------------------------------------------------------------------------------------------------------------------

def LB_WC_STHE(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound using the value of the minimum water flowrate used for Proxy Set Trimming
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)
    Fw_fixed = max(m_p['Fw_Thi_min'], m_p['Fw_Tco_min'])

    Fw_PST_min = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), np.maximum(Fw_fixed, Fw_pass_min))

    LB = Calculations_WC_STHE_TAC.WC_STHE_TAC(Fw_PST_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp, lay, L,
                                              m_p['pcw'], m_p['pc'], m_p['roc'], m_p['eta'], m_p['cf'], m_p['cv'],
                                              m_p['alpha'], m_p['Nop'], m_p['int_rate'], m_p['n'], m_p, m_p['ms'],
                                              m_p['ros'], m_p['mis'], Nb, Bc)
    return LB

# endregion

######################################################################################################################

# region OF function
# --------------------------------------------------------------------------------------------------------------------
# Objective Function
# --------------------------------------------------------------------------------------------------------------------

def TAC_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Objective function
    Fw_hat = Calculations_WC_STHE_flowrates.WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, m_p['vtmin'], m_p['roc'],
                                                           m_p['thk'], m_p['Retmin'], m_p['mic'], m_p['Fw_Thi_min'],
                                                           m_p['Xp'], m_p['Fw_Tco_min'], m_p['mh'], m_p['Cph'],
                                                           m_p['Thi'], m_p['Tho'], m_p['Cpc'], m_p['Tci'], m_p['rot'],
                                                           m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'], m_p['ms'],
                                                           m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                           m_p['ktube'], m_p['yfluid'], m_p['Aexc'], m_p['vtmax'],
                                                           m_p['Retmax'], m_p['Fw_max'], Bc, m_p)
    #print('Fw_hat_OF', Fw_hat)
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    #print('Fw_vel_min_OF', Fw_vel_min)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    #print('Fw_Re_min_OF', Fw_Re_min)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)

    #Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), Fw_fixed)
    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), np.maximum(m_p['Fw_Tco_min'], Fw_pass_min))
    #print('Fw_Tco_min_OF', m_p['Fw_Tco_min'])
    #print('Fw_pass_min_OF', Fw_pass_min)
    #print('Fw_water_OF', Fw_min)

    # Calculating Tco
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    m_p['m_water'] = Fw_min
    Tco = Q/(m_p['Cpc']*m_p['m_water']) + m_p['Tci']
    #print('Tco_OF', Tco)
    #m_p['Tco'] = Tco

    # Calculations for print
    #ht = Calculations_STHE_htubeside.STHE_h_tubeside(Fw_min, m_p['rot'], m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['thk'],
    #                                                 m_p['yfluid'], Ds, dte, Npt, rp, lay, L, m_p)
    #print('ht', ht)
    #vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(Fw_min, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
    #                                                                lay, m_p)
    #print('vt', vt)
    # #DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(Fw_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp, lay, L, m_p)
    # #print('DPt', DPt)
    # LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], Tco)
    # print('LMTD', LMTD)
    # U = Calculations_STHE_U.STHE_overall_coefficient(Fw_min, m_p['rot'], m_p['Cpt'], m_p['mit'], m_p['kt'],
    #                                                  m_p['Rft'], m_p['ms'], m_p['ros'], m_p['Cps'], m_p['mis'],
    #                                                  m_p['ks'], m_p['Rfs'], m_p['thk'], m_p['ktube'], m_p['yfluid'], Ds,
    #                                                  dte, Npt, rp, lay, L, Nb, Bc, m_p)
    # print('U', U)
    # Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(Fw_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds,
    #                                                                  dte, Npt, rp, lay, m_p)
    # print('Ret', Ret)

    OF_Solution = Calculations_WC_STHE_TAC.WC_STHE_TAC(Fw_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp,
                                                       lay, L, m_p['pcw'], m_p['pc'], m_p['roc'], m_p['eta'], m_p['cf'],
                                                       m_p['cv'], m_p['alpha'], m_p['Nop'], m_p['int_rate'], m_p['n'],
                                                       m_p, m_p['ms'], m_p['ros'], m_p['mis'], Nb, Bc)
    return OF_Solution

# endregion

#######################################################################################################################

# region Smart Enumeration Constraints
# -------------------------------------------------------------------------------------------------------------------
# Smart Enumeration Functions
# -------------------------------------------------------------------------------------------------------------------

def Fw_ub_SE(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Fw_hat = Calculations_WC_STHE_flowrates.WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, m_p['vtmin'], m_p['roc'],
                                                           m_p['thk'], m_p['Retmin'], m_p['mic'], m_p['Fw_Thi_min'],
                                                           m_p['Xp'], m_p['Fw_Tco_min'], m_p['mh'], m_p['Cph'],
                                                           m_p['Thi'], m_p['Tho'], m_p['Cpc'], m_p['Tci'], m_p['rot'],
                                                           m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'], m_p['ms'],
                                                           m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                           m_p['ktube'], m_p['yfluid'], m_p['Aexc'], m_p['vtmax'],
                                                           m_p['Retmax'], m_p['Fw_max'], Bc, m_p)
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)
    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)

    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), np.maximum(m_p['Fw_Tco_min'], Fw_pass_min))
    #print('Fw_min_SE', Fw_min)

    fun_val_SE = Fw_min - m_p['Fw_max']

    return fun_val_SE

def vt_ub_SE(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vt
    Fw_hat = Calculations_WC_STHE_flowrates.WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, m_p['vtmin'], m_p['roc'],
                                                           m_p['thk'], m_p['Retmin'], m_p['mic'], m_p['Fw_Thi_min'],
                                                           m_p['Xp'], m_p['Fw_Tco_min'], m_p['mh'], m_p['Cph'],
                                                           m_p['Thi'], m_p['Tho'], m_p['Cpc'], m_p['Tci'], m_p['rot'],
                                                           m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'], m_p['ms'],
                                                           m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                           m_p['ktube'], m_p['yfluid'], m_p['Aexc'], m_p['vtmax'],
                                                           m_p['Retmax'], m_p['Fw_max'], Bc, m_p)
    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)

    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)

    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), np.maximum(m_p['Fw_Tco_min'], Fw_pass_min))

    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(Fw_min, m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p)
    fun_val_SE = vt - m_p['vtmax']
    return fun_val_SE

def Ret_ub_SE(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on Ret
    Fw_hat = Calculations_WC_STHE_flowrates.WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, m_p['vtmin'], m_p['roc'],
                                                           m_p['thk'], m_p['Retmin'], m_p['mic'], m_p['Fw_Thi_min'],
                                                           m_p['Xp'], m_p['Fw_Tco_min'], m_p['mh'], m_p['Cph'],
                                                           m_p['Thi'], m_p['Tho'], m_p['Cpc'], m_p['Tci'], m_p['rot'],
                                                           m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'], m_p['ms'],
                                                           m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                           m_p['ktube'], m_p['yfluid'], m_p['Aexc'], m_p['vtmax'],
                                                           m_p['Retmax'], m_p['Fw_max'], Bc, m_p)

    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)

    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)

    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), np.maximum(m_p['Fw_Tco_min'], Fw_pass_min))

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(Fw_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds,
                                                                     dte, Npt, rp, lay, m_p)
    fun_val_SE = Ret - m_p['Retmax']
    return fun_val_SE

def DPt_ub_SE(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on DPt
    Fw_hat = Calculations_WC_STHE_flowrates.WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, m_p['vtmin'], m_p['roc'],
                                                           m_p['thk'], m_p['Retmin'], m_p['mic'], m_p['Fw_Thi_min'],
                                                           m_p['Xp'], m_p['Fw_Tco_min'], m_p['mh'], m_p['Cph'],
                                                           m_p['Thi'], m_p['Tho'], m_p['Cpc'], m_p['Tci'], m_p['rot'],
                                                           m_p['Cpt'], m_p['mit'], m_p['kt'], m_p['Rft'], m_p['ms'],
                                                           m_p['ros'], m_p['Cps'], m_p['mis'], m_p['ks'], m_p['Rfs'],
                                                           m_p['ktube'], m_p['yfluid'], m_p['Aexc'], m_p['vtmax'],
                                                           m_p['Retmax'], m_p['Fw_max'], Bc, m_p)

    Fw_vel_min = Calculations_WC_STHE_flowrates.WC_Fw_vel_min(m_p['vtmin'], Npt, dte, m_p['roc'], m_p['thk'], Ds,
                                                              rp, lay, m_p)
    Fw_Re_min = Calculations_WC_STHE_flowrates.WC_Fw_Re_min(m_p['Retmin'], Npt, dte, m_p['thk'], m_p['mic'], Ds,
                                                            rp, lay, m_p)

    Fw_pass_min = Calculations_WC_STHE_flowrates.WC_Fw_pass_min(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'],
                                                                m_p['Cpc'], m_p['Tci'], m_p['Xp'], Npt)

    Fw_min = np.maximum(np.maximum(Fw_hat, Fw_vel_min, Fw_Re_min), np.maximum(m_p['Fw_Tco_min'], Fw_pass_min))

    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(Fw_min, m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte,
                                                                Npt, rp, lay, L, m_p)
    #print('DPt', DPt)
    fun_val_SE = DPt - m_p['DPtdisp']
    return fun_val_SE

# endregion

