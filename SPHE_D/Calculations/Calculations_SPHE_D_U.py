#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Support direct and geometry-based U calculations
##################################################################################################################
#endregion

#region Import Library
from SPHE_D.Calculations import Calculations_SPHE_D_h, Calculations_SPHE_D_Area
#endregion

#region Calculations

def SPHE_overall_coefficient(*args):
    """
    Calculate the overall heat-transfer coefficient.

    Supported signatures
    --------------------
    SPHE_overall_coefficient(h_I, h_II, thk, Rfh, Rfc, kplate)
        Direct calculation from channel coefficients.
    SPHE_overall_coefficient(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate)
        Geometry-based calculation for the current Set Trimming model.
    """
    if len(args) == 6:
        h_I, h_II, thk, Rfh, Rfc, kplate = args
        return 1 / (1 / h_I + Rfh + thk / kplate + 1 / h_II + Rfc)

    if len(args) == 17:
        L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate = args
        hh, hc = Calculations_SPHE_D_h.SPHE_h(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc)
        return 1 / (1 / hh + Rfh + thk / kplate + 1 / hc + Rfc)

    raise TypeError("SPHE_overall_coefficient expects either 6 direct arguments or 17 geometry-based arguments.")


def SPHE_overall_coefficient_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate):
    """Return an upper-bound estimate for the overall heat-transfer coefficient."""
    hhub, hcub = Calculations_SPHE_D_h.SPHE_h_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax)
    return 1 / (1 / hhub + Rfh + thk / kplate + 1 / hcub + Rfc)


def SPHE_Qspec(mh, Thtarget, Thi, Cph):
    """Return specified duty from hot-stream target temperature."""
    return mh * (Thi - Thtarget) * Cph


def SPHE_Qub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate):
    """Return a rough upper-bound duty estimate."""
    Uub = SPHE_overall_coefficient_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate)
    A = Calculations_SPHE_D_Area.SPHE_area(L, H)
    LMTDub = 100
    return Uub * A * LMTDub

#endregion
