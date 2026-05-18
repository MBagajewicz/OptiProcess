#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

# region Import Library
from Common_Equations_HEX import Calculations_HEX_heatload
import numpy as np
#endregion


#region Calculations
def Airpreheater_epsilon_Nutcalc(X, mh, Cph, Thi, Tho, Tci, mc, Cpc):  # Required nut calculation for a given service
    nut_c = X[0]
    pc = X[1]
    pp = X[2]

    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    Qmax = mh * Cph * (Thi - Tci)
    RCi = mh * Cph / mc / Cpc / 2
    RC = mh * Cph / mc / Cpc
    effetv = Q / Qmax
    f1 = (1 - np.exp(-nut_c * (1 - RCi))) / (1 - RCi * np.exp(-nut_c * (1 - RCi))) - pc
    f2 = (1 - np.exp(-nut_c * (1 + RCi))) / (1 + RCi) - pp
    f3 = 0.5 * (pc + pp - 0.5 * pc * pp * RC) - effetv
    f = [f1, f2, f3]
    return f

#endregion