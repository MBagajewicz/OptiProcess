#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Support length-based and turn-based SPHE area calls
##################################################################################################################
#endregion

#region Import Library
from SPHE_D.Calculations.Calculations_SPHE_D_Length import SPHE_spiral_length
#endregion

#region Calculations

def SPHE_area(*args):
    """
    Calculate the SPHE heat-transfer area.

    Supported signatures
    --------------------
    SPHE_area(L, H)
        Length-based model used by the current Set Trimming variables.
    SPHE_area(N, ds, d_I, d_II, tk, H)
        Turn-based model used by the distributed-temperature formulation.
    """
    if len(args) == 2:
        L, H = args
        return 2 * H * L

    if len(args) == 6:
        N, ds, d_I, d_II, tk, H = args
        L = SPHE_spiral_length(N, ds, d_I, d_II, tk)
        return 2 * H * L

    raise TypeError("SPHE_area expects either (L, H) or (N, ds, d_I, d_II, tk, H).")

#endregion
