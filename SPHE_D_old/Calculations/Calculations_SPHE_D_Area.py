#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
##################################################################################################################
#endregion


#region Import Library
from SPHE_D.Calculations.Calculations_SPHE_D_Length import SPHE_spiral_length
#endregion

#region Calculations

def SPHE_area(N, ds, d_I, d_II, tk, H):
    # Spiral length
    L = SPHE_spiral_length(N, ds, d_I, d_II, tk)
    # Heat exchanger area
    A = 2 * H * L
    return A