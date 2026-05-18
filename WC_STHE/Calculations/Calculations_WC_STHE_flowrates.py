##################################################################################################################
# region Titles and Header
# Nature: Setting
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       06-Feb-2025       Mariana Mello               Proposed
#   0.2       23-Apr-2025       Mariana Mello               Update to fix error
#   0.3       06-May-2025       Mariana Mello               Revision from paper
#   0.4       12-May-2025       Mariana Mello               Changed name from 'pd' to 'm_p'
#   0.5       06-Jun-2025       Mariana Mello               Changed Fw_pass_min and Fw_hat
##################################################################################################################
# endregion

# region Import Library
from STHE.Calculations import (
    Calculations_STHE_U,
    Calculations_STHE_correction_factor,
    Calculations_STHE_area,
    Calculations_STHE_countingtable)
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
from math import pi
import numpy as np
#from scipy.optimize import root_scalar
#from scipy.optimize import bisect
from scipy.optimize import newton
# endregion
######################################################################################################################

# region Calculations

def WC_Fw_param(mh, Cph, Thi, Tho, Cpc, Tci, T_param):
    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    Fw_param = Q/(Cpc*(T_param-Tci))
    return Fw_param

def WC_Fw_vel_min(vtmin, Npt, Dte, roc, thk, Ds, rp, lay, m_p):
    Dti = Dte - 2*thk
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, Dte, Npt, rp, lay, m_p)
    Ntp = Ntt / Npt
    Fw_vel_min = vtmin*Ntp*((pi*(Dti**2))/4)*roc
    return Fw_vel_min

def WC_Fw_pass_min(mh, Cph, Thi, Tho, Cpc, Tci, Xp, Npt):
    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    Fw_pass_min = (Q/(2*Cpc)) * ((((Thi - Tho) / (Thi - Tci)) - 2*Xp)/(Xp*(Thi - Tho) - (Xp**2) * (Thi - Tci)))*np.ones(Npt.shape)
    Fw_pass_min[Npt == 1] = 0
    return Fw_pass_min

def WC_Fw_vel_max(vtmax, Npt, Dte, roc, thk, Ds, rp, lay, m_p):
    Dti = Dte - 2*thk
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, Dte, Npt, rp, lay, m_p)
    Ntp = Ntt / Npt
    Fw_vel_max = vtmax*Ntp*((pi*(Dti**2))/4)*roc
    return Fw_vel_max

def WC_Fw_Re_min(Retmin, Npt, Dte, thk, mic, Ds, rp, lay, m_p):
    Dti = Dte - 2 * thk
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, Dte, Npt, rp, lay, m_p)
    Ntp = Ntt / Npt
    Fw_Re_min = (Retmin*pi*mic*Dti*Ntp)/4
    return Fw_Re_min

def WC_Fw_Re_max(Retmax, Npt, Dte, thk, mic, Ds, rp, lay, m_p):
    Dti = Dte - 2 * thk
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, Dte, Npt, rp, lay, m_p)
    Ntp = Ntt / Npt
    Fw_Re_max = (Retmax*pi*mic*Dti*Ntp)/4
    return Fw_Re_max


def WC_STHE_Fw_hat_bounds(Ds, dte, Npt, rp, lay, L, Nb, vtmin, roc, thk, Retmin, mic, Fw_Thi_min, Xp, Fw_Tco_min, mh,
                          Cph, Thi, Tho, Cpc, Tci, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, ktube, yfluid, Aexc,
                          vtmax, Retmax, Fw_max, Bc, m_p):

    # Step 0: Defining the parts of the equation
    def eq_left(Fw):
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        Tco = (Q / (Cpc * Fw)) + Tci
        #print('Tco',Tco)
        U = Calculations_STHE_U.STHE_overall_coefficient(Fw, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, thk,
                                                         ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
        #print('U', U)
        F = Calculations_STHE_correction_factor.STHE_correction_factor(Thi, Tho, Tci, Tco, Npt, m_p['Xp'])
        #print('F', F)
        LMTD = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
        #print('LMTD', LMTD)
        equation_left = U * F * LMTD
        return equation_left

    def eq_right():
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        #print('Q',Q)
        A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
        #print('A',A)
        equation_right = ((1 + Aexc / 100) * Q) / A
        return equation_right

    # Step 1: Calculate the Fw_LB that is the Lower Bound for Fw_hat

    # Calculate the minimum flowrate
    Fw_vel_min = WC_Fw_vel_min(vtmin, Npt, dte, roc, thk, Ds, rp, lay, m_p)
    Fw_Re_min = WC_Fw_Re_min(Retmin, Npt, dte, thk, mic, Ds, rp, lay, m_p)
    Fw_pass_min = WC_Fw_pass_min(mh, Cph, Thi, Tho, Cpc, Tci, Xp, Npt)
    Fw_fixed = max(Fw_Thi_min, Fw_Tco_min)
    Fw_LB = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), np.maximum(Fw_fixed, Fw_pass_min))
    #print('Fw_LB', Fw_LB)

    # Step 2: Calculate the Fw_UB that is the Upper Bound for Fw_hat

    # Calculate the maximum flowrates
    Fw_vel_max = WC_Fw_vel_max(vtmax, Npt, dte, roc, thk, Ds, rp, lay, m_p)
    Fw_Re_max = WC_Fw_Re_max(Retmax, Npt, dte, thk, mic, Ds, rp, lay, m_p)
    Fw_UB = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), Fw_max)
    #print('Fw_UB', Fw_UB)

    # Step 3: Verification
    if Fw_LB > Fw_UB:
       #print('The problem has no solution, Fw_LB>Fw_UB')
       return 1e20, 1e20

    # Step 4: Calculations with Fw_UB(max)
    eq_left_FwUB = eq_left(Fw_UB)
    #print('LEFT', eq_left(Fw_UB))
    eq_right_FwUB = eq_right()
    #print('RIGHT', eq_right())

    # Verification: left > right -> ok
    if eq_left_FwUB > eq_right_FwUB:
        Fw_solution_UB = Fw_UB
        return Fw_LB, Fw_UB

    elif eq_left_FwUB < eq_right_FwUB:
        #print('The equation of Fw_hat has no solution')
        return 1e20, 1e20

def WC_STHE_Fw_hat(Ds, dte, Npt, rp, lay, L, Nb, vtmin, roc, thk, Retmin, mic, Fw_Thi_min, Xp, Fw_Tco_min,
                   mh, Cph, Thi, Tho, Cpc, Tci, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, ktube, yfluid,
                   Aexc, vtmax, Retmax, Fw_max, Bc, m_p):

    def f_Fw_hat(Fw):
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
        Tco = (Q / (Cpc * Fw)) + Tci
        U = Calculations_STHE_U.STHE_overall_coefficient(Fw, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, thk,
                                                         ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
        F = Calculations_STHE_correction_factor.STHE_correction_factor(Thi, Tho, Tci, Tco, Npt, m_p['Xp'])
        LMTD = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
        return (U * F * LMTD) - (((1 + Aexc / 100) * Q) / A)

    # Bounds
    a, b = WC_STHE_Fw_hat_bounds(Ds, dte, Npt, rp, lay, L, Nb, vtmin, roc, thk, Retmin, mic, Fw_Thi_min, Xp,
                                 Fw_Tco_min, mh, Cph, Thi, Tho, Cpc, Tci, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis,
                                 ks, Rfs, ktube, yfluid, Aexc, vtmax, Retmax, Fw_max, Bc, m_p)

    #print('Fw_LB_Fwhat and Fw_UB_Fwhat', a, b)
    if a and b == 1e20:
        return 1e20
    else:
        #solution = bisect(f_Fw_hat, a, b)
        solution = newton(f_Fw_hat, a)
        return solution
