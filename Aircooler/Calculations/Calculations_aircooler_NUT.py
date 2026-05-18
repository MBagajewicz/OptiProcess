#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Import Library
from Aircooler.Calculations import Calculations_aircooler_prop_cpc, Calculations_aircooler_mc
import numpy as np
from scipy.optimize import root_scalar
#endregion


#region Calculations

def aircooler_NUT(Thi, Tho, Tci, mh, Cph, Tco):
    Cpc = Calculations_aircooler_prop_cpc.aircooler_calc_prop_air_Cpc(Tco, Tci)
    mc = Calculations_aircooler_mc.aircooler_mc(mh, Cph, Thi, Tho, Tco, Tci)
    # NUT - Number of transfer units
    # E (epsilon) - heat exchanger effectiveness
    epsilon = (Thi - Tho)/(Thi - Tci)
    # Cr - ratio between heat capacity flow rates
    Cr = (mh*Cph)/(mc*Cpc)
    def f_nut(NUT):
        return (1 - np.exp((1 / Cr) * (NUT ** 0.22) * (np.exp(-Cr * (NUT ** 0.78)) - 1)) - epsilon)
    solution = root_scalar(f_nut, bracket=[1e-6, 50])
    return solution.root

#endregion