#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
###################################################################################################################
#endregion


#region Import Library
from SPHE_LMTD.Calculations import (Calculations_SPHE_LMTD_DeltaP, Calculations_SPHE_LMTD_area)
#endregion

#region Calculations

def SPHE_TAC(int_rate, n, par_a, par_b, H, L, pc, eta, mh, mc, roh, roc, dh, dc, mih, mic, Nop):

    r = ((int_rate*(1+int_rate)**n))/(((1+int_rate)**n) - 1) # Af=i*((1+i)**ny)/((1+i)**ny-1);
    A = Calculations_SPHE_LMTD_area.SPHE_area(L, H)
    Costcap = par_a * ( A ** par_b)

    dltph, _ = Calculations_SPHE_LMTD_DeltaP.SPHE_DeltaP(L, roh, roc, mh, mc, H, dh, dc, mih, mic)
    _, dltpc = Calculations_SPHE_LMTD_DeltaP.SPHE_DeltaP(L, roh, roc, mh, mc, H, dh, dc, mih, mic)
    Costope = Nop * (pc / 1000) * (1 / eta) * ((mh * dltph * 6895) / roh + (mc * dltpc * 6895) / roc)

    TAC = r * Costcap + Costope

    return TAC


def SPHE_TAC_distributed(int_rate, n, par_a, par_b, H, L, pc, eta, mh, mc, roh, roc, dh, dc, mih, mic, Nop):

    r = ((int_rate*(1+int_rate)**n))/(((1+int_rate)**n) - 1) # Af=i*((1+i)**ny)/((1+i)**ny-1);
    A = Calculations_SPHE_LMTD_area.SPHE_area(L, H)
    Costcap = par_a * ( A ** par_b)

# I should call the pressure drop calculated by the nonlinear ODE model here, but I don't know how to call it.
    #dltph = .......
    #dltpc = .......
    dltph = 1
    dltpc = 1

    Costope = Nop * (pc / 1000) * (1 / eta) * ((mh * dltph * 6895) / roh + (mc * dltpc * 6895) / roc)

    TAC_distributed = r * Costcap + Costope

    return TAC_distributed
#endregion