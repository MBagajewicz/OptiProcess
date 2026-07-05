#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Use SPHE_D namespace consistently
##################################################################################################################
#endregion

#region Import Library
from SPHE_D.Calculations import Calculations_SPHE_D_DeltaP, Calculations_SPHE_D_Area
#endregion

#region Calculations

def SPHE_TAC(int_rate, n, par_a, par_b, H, L, pc, eta, mh, mc, roh, roc, dh, dc, mih, mic, Nop):
    """Calculate the total annualized cost for the length-based SPHE model."""
    r = (int_rate * (1 + int_rate) ** n) / (((1 + int_rate) ** n) - 1)
    A = Calculations_SPHE_D_Area.SPHE_area(L, H)
    Costcap = par_a * (A ** par_b)

    dltph, dltpc = Calculations_SPHE_D_DeltaP.SPHE_DeltaP(L, roh, roc, mh, mc, H, dh, dc, mih, mic)
    Costope = Nop * (pc / 1000) * (1 / eta) * ((mh * dltph) / roh + (mc * dltpc) / roc)

    return r * Costcap + Costope


def SPHE_TAC_distributed(int_rate, n, par_a, par_b, H, L, pc, eta, mh, mc, roh, roc, dh, dc, mih, mic, Nop):
    """Placeholder TAC for distributed-temperature calculations."""
    r = (int_rate * (1 + int_rate) ** n) / (((1 + int_rate) ** n) - 1)
    A = Calculations_SPHE_D_Area.SPHE_area(L, H)
    Costcap = par_a * (A ** par_b)

    dltph = 1
    dltpc = 1
    Costope = Nop * (pc / 1000) * (1 / eta) * ((mh * dltph) / roh + (mc * dltpc) / roc)

    return r * Costcap + Costope

#endregion
