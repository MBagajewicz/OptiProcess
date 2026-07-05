#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Support scalar-channel and geometry-based calls
##################################################################################################################
#endregion

#region Import Library
import numpy as np
#endregion

#region Calculations

def SPHE_spiral_outer_diameter(L, dh, dc, thk, ds):
    """Return the spiral outer diameter for the length-based SPHE model."""
    return np.sqrt(1.28 * L * (dh + dc + 2 * thk) + ds**2)


def SPHE_critical_reynolds(Dh, Ds):
    """Return the critical Reynolds number for spiral channels."""
    return 20000 * ((Dh / Ds) ** 0.32)


def SPHE_Reynolds(*args):
    """
    Calculate Reynolds numbers.

    Supported signatures
    --------------------
    SPHE_Reynolds(Dh, G, mi)
        Single-channel Reynolds number.
    SPHE_Reynolds(dh, dc, H, mh, mc, mih, mic, L, thk, ds)
        Returns (Reh, Rec, Reeh, Reec) for the length-based SPHE model.
    """
    if len(args) == 3:
        Dh, G, mi = args
        return Dh * G / mi

    if len(args) == 10:
        dh, dc, H, mh, mc, mih, mic, L, thk, ds = args
        Ds = SPHE_spiral_outer_diameter(L, dh, dc, thk, ds)
        Dh = 2 * dh * H / (dh + H)
        Dc = 2 * dc * H / (dc + H)
        Gh = mh / (dh * H)
        Gc = mc / (dc * H)
        Reh = Dh * Gh / mih
        Rec = Dc * Gc / mic
        Reeh = SPHE_critical_reynolds(Dh, Ds)
        Reec = SPHE_critical_reynolds(Dc, Ds)
        return Reh, Rec, Reeh, Reec

    raise TypeError("SPHE_Reynolds expects either (Dh, G, mi) or (dh, dc, H, mh, mc, mih, mic, L, thk, ds).")


def SPHE_Reynolds_ub(dh, dc, H, mh, mc, mimin, L, thk, ds):
    """Return upper-bound Reynolds estimates and critical Reynolds values."""
    Ds = SPHE_spiral_outer_diameter(L, dh, dc, thk, ds)
    Dh = 2 * dh * H / (dh + H)
    Dc = 2 * dc * H / (dc + H)
    Gh = mh / (dh * H)
    Gc = mc / (dc * H)

    Rehub = Dh * Gh / mimin
    Recub = Dc * Gc / mimin
    Reeh = SPHE_critical_reynolds(Dh, Ds)
    Reec = SPHE_critical_reynolds(Dc, Ds)

    return Rehub, Recub, Reeh, Reec

#endregion
