##################################################################################################################
# region Titles and Header
# Nature: Setting
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       19-Mar-2025       Mariana Mello               Proposed
#   0.2       12-May-2025       Mariana Mello               Revision
#   0.3       23-Sep-2025       Mariana Mello               Revision
##################################################################################################################
# endregion

# region Import Library
from GPHE.Calculations import (
    Calculations_GPHE_U,
    Calculations_GPHE_epsilon_Nutcalc,
    Calculations_GPHE_correction_factor,
    Calculations_GPHE_area
    )
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
#from math import pi
import numpy as np
from scipy import optimize
from scipy.optimize import root_scalar
from scipy.optimize import bisect
from scipy.optimize import newton
# endregion


def WC_Fw_param(mh, Cph, Thi, Tho, Cpc, Tci, T_param):
    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    Fw_param = Q/(Cpc*(T_param-Tci))
    return Fw_param

def WC_Fw_vel_min(Ntp, Npc, bp, Lw, vcmin, roc):
    Ncp = (Ntp - 1)/2*Npc
    Ac = bp*Lw
    Fw_vel_min = vcmin*roc*Ac*Ncp
    return Fw_vel_min

def WC_Fw_vel_max(Ntp, Npc, bp, Lw, vcmax, roc):
    Ncp = (Ntp - 1)/2*Npc
    Ac = bp*Lw
    Fw_vel_max = vcmax*roc*Ac*Ncp
    return Fw_vel_max

def WC_Fw_Re_min(Ntp, Npc, bp, phi, Lw, mic, Retmin):
    Ncp = (Ntp - 1)/(2*Npc)
    Deq = 2*bp/phi
    Ac = bp*Lw
    Fw_Re_min = (Retmin*mic*Ac*Ncp)/Deq
    return Fw_Re_min

def WC_Fw_Re_max(Ntp, Npc, bp, phi, Lw, mic, Retmax):
    Ncp = (Ntp - 1)/(2*Npc)
    Deq = 2*bp/phi
    Ac = bp*Lw
    Fw_Re_max = (Retmax*mic*Ac*Ncp)/Deq
    return Fw_Re_max

def WC_Fw_hat_bounds(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc, Cph, mic, mih, kc, kh,
                     roc, roh, mh, Thi, Tho, Tci, Aexc, vcmin, Retmin, Fw_Thi_min, Fw_Tco_min,
                     vcmax, Retmax, Fw_max):
    # Step 0: Defining the parts of the equation
    def eq_left(Fw):
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        Tco = (Q / (Cpc * Fw)) + Tci
        U = Calculations_GPHE_U.GPHE_overall_coefficient(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc,
                                                         Cph, mic, mih, kc, kh, roc, roh, Fw, mh)
        LMTD = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
        # xo = np.array([1, 0.8, 0.9])
        # xsol = optimize.root(Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc, xo,
        #                      args=(mh, Cph, Thi, Tho, Tci, Fw, Cpc))
        # F1_2 = (Thi - Tho) / LMTD / xsol.x[0]
        tam = len(Fw)
        xo = np.ones((3, tam))
        solutions = []
        for i in range(tam):
            x0_set = xo[:, i]
            Fw_i = Fw[i]

            sol = optimize.root(Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc, x0_set,
                                args=(mh, Cph, Thi, Tho, Tci, Fw_i, Cpc))
            solutions.append(sol.x)
        solutions = np.array(solutions).T
        F1_2 = (Thi - Tho) / LMTD / solutions[0, :]
        F = Calculations_GPHE_correction_factor.GPHE_correction_factor(Thi, Tho, Tci, Tco, Nph, Npc, F1_2)
        equation_left = U * F * LMTD
        return equation_left

    def eq_right():
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        NTP_termicos = Ntp - 2
        Atermica = Calculations_GPHE_area.GPHE_area(phi, NTP_termicos, Lp, Lw)
        equation_right = ((1 + Aexc / 100) * Q) / Atermica
        return equation_right

    # Step 1: Calculate the Fw_LB that is the Lower Bound
    # Calculate the minimum flowrates
    Fw_vel_min = WC_Fw_vel_min(Ntp, Npc, bp, Lw, vcmin, roc)
    Fw_Re_min = WC_Fw_Re_min(Ntp, Npc, bp, phi, Lw, mic, Retmin)
    Fw_fixed = max(Fw_Thi_min, Fw_Tco_min)
    Fw_LB = np.maximum(np.maximum(Fw_vel_min, Fw_Re_min), Fw_fixed)
    #print('LB', Fw_LB)

    # Step 2: Calculate the Fw_UB that is the Upper Bound
    # Calculate the maximum flowrates
    Fw_vel_max = WC_Fw_vel_max(Ntp, Npc, bp, Lw, vcmax, roc)
    Fw_Re_max = WC_Fw_Re_max(Ntp, Npc, bp, phi, Lw, mic, Retmax)
    Fw_UB = np.minimum(np.minimum(Fw_vel_max, Fw_Re_max), Fw_max)
    #print('UB', Fw_UB)

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

def WC_Fw_hat(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc, Cph, mic, mih, kc, kh, roc, roh,
              mh, Thi, Tho, Tci, Aexc, vcmin, Retmin, Fw_Thi_min, Fw_Tco_min, vcmax, Retmax, Fw_max):

    def f_Fw_hat(Fw):
        Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
        NTP_termicos = Ntp - 2
        Atermica = Calculations_GPHE_area.GPHE_area(phi, NTP_termicos, Lp, Lw)
        Tco = (Q / (Cpc * Fw)) + Tci
        U = Calculations_GPHE_U.GPHE_overall_coefficient(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc,
                                                         Cph, mic, mih, kc, kh, roc, roh, Fw, mh)
        LMTD = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
        xo = np.array([1, 0.8, 0.9])
        xsol = optimize.root(
            lambda X, *args: Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc(X, *args).ravel(),
            xo, args=(mh, Cph, Thi, Tho, Tci, Fw, Cpc))
        # xsol = optimize.root(Calculations_GPHE_epsilon_Nutcalc.GPHE_epsilon_Nutcalc, xo,
        #                      args=(mh, Cph, Thi, Tho, Tci, Fw, Cpc))
        F1_2 = (Thi - Tho) / LMTD / xsol.x[0]
        F = Calculations_GPHE_correction_factor.GPHE_correction_factor(Thi, Tho, Tci, Tco, Nph, Npc, F1_2)
        return (U * F * LMTD) - (((1 + Aexc / 100) * Q) / Atermica)

    # Bounds
    a, b = WC_Fw_hat_bounds(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc, Cph, mic, mih, kc,
                            kh, roc, roh, mh, Thi, Tho, Tci, Aexc, vcmin, Retmin, Fw_Thi_min, Fw_Tco_min,
                            vcmax, Retmax, Fw_max)

    #print('Fw_LB and Fw_UB', a, b)
    if a and b == 1e20:
        return 1e20
    else:
        #solution = bisect(f_Fw_hat, a, b)
        solution = newton(f_Fw_hat, a)
        return solution

