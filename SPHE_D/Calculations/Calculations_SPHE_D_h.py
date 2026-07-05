#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Support Nusselt-based and geometry-based calls
#################################################################################################################
#endregion

#region Import Library
from SPHE_D.Calculations import Calculations_SPHE_D_Reynolds
#endregion

#region Calculations

def SPHE_h(*args):
    """
    Calculate convective heat-transfer coefficients.

    Supported signatures
    --------------------
    SPHE_h(Nu, k, Dh)
        Direct coefficient from Nusselt number.
    SPHE_h(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc)
        Returns (hh, hc) for the length-based SPHE model.
    """
    if len(args) == 3:
        Nu, k, Dh = args
        return Nu * k / Dh

    if len(args) == 14:
        L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc = args
        Dh = 2 * dh * H / (dh + H)
        Dc = 2 * dc * H / (dc + H)
        Ds = Calculations_SPHE_D_Reynolds.SPHE_spiral_outer_diameter(L, dh, dc, thk, ds)
        Gh = mh / (dh * H)
        Gc = mc / (dc * H)
        Prh = mih * Cph / kh
        Prc = mic * Cpc / kc
        Reh, Rec, _, _ = Calculations_SPHE_D_Reynolds.SPHE_Reynolds(dh, dc, H, mh, mc, mih, mic, L, thk, ds)

        hh = (1 + 3.54 * Dh / Ds) * 0.023 * Cph * Gh * (Reh ** (-0.2)) * (Prh ** (-2 / 3))
        hc = (1 + 3.54 * Dc / Ds) * 0.023 * Cpc * Gc * (Rec ** (-0.2)) * (Prc ** (-2 / 3))
        return hh, hc

    raise TypeError("SPHE_h expects either (Nu, k, Dh) or (L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc).")


def SPHE_h_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax):
    """Return upper-bound heat-transfer coefficients for both channels."""
    Dh = 2 * dh * H / (dh + H)
    Dc = 2 * dc * H / (dc + H)
    Ds = Calculations_SPHE_D_Reynolds.SPHE_spiral_outer_diameter(L, dh, dc, thk, ds)
    Gh = mh / (dh * H)
    Gc = mc / (dc * H)

    hhub = (1 + 3.54 * Dh / Ds) * 0.023 * (Gh ** 0.8) * (Dh ** (-0.2)) * (Cpmax ** (1 / 3)) * (mimin ** (-7 / 15)) * (kmax ** (2 / 3))
    hcub = (1 + 3.54 * Dc / Ds) * 0.023 * (Gc ** 0.8) * (Dc ** (-0.2)) * (Cpmax ** (1 / 3)) * (mimin ** (-7 / 15)) * (kmax ** (2 / 3))

    return hhub, hcub

#endregion
