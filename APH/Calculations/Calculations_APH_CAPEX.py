#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          21-Oct-2025     Sung Young Kim            Copy from STHE folder
##################################################################################################################
#endregion


#region Import Library
from APH.Calculations import Calculations_APH_area
#endregion

#region Calculations

def APH_CAPEX(Do, lf, Nc, Nr, L, Nf, tf, Ncross, par_a, par_b):
    # Area
    area_tot = Calculations_APH_area.APH_area_tot(Do, lf, Nc, Nr, L, Nf, tf, Ncross)
    # Capital cost
    Cap = par_a*(area_tot**par_b)
    return Cap

#endregion