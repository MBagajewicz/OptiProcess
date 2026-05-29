#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          26-Mar-2025     Mariana Mello              Proposed

##################################################################################################################
#endregion


#region Import Library
from GPHE.Calculations import Calculations_GPHE_area
#endregion
#######################################################################################################################

#region Calculations

def GPHE_CAPEX(Ntp, Lp, Lw, par_a, par_b, phi):
    Atot = Calculations_GPHE_area.GPHE_area(phi, Ntp, Lp, Lw)
    Cap = par_a*(Atot**par_b)   # Capital cost
    return Cap

#endregion