#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          24-Mar-2024     Mariana Mello             Proposed
#   0.2          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
##################################################################################################################
#endregion


#region Import Library
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_area
#endregion

#region Calculations

def SPHE_LMTD_CAPEX(par_a, par_b, L, H):
    # Area
    Atot = Calculations_SPHE_LMTD_area.SPHE_LMTD_area(L, H)
    # Capital cost
    Cap = par_a*(Atot**par_b)
    return Cap

#endregion