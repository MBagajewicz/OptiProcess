#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion


#region Import Library
from Kettle.Calculations import Calculations_Kettle_Nusselt_shellside
from math import pi
import numpy as np
#endregion

#region Calculations

def Kettle_h_shellside(ms, ros, Cps, mis, ks, Ds, dte, rp, lay, L, Nb):
    Nus = Calculations_Kettle_Nusselt_shellside.Kettle_Nusselt_shellside(ms, ros, Cps, mis, ks, Ds, dte, rp, lay, L, Nb)
    K_Deq = 4 * np.ones(lay.shape)
    if isinstance(lay,float) or isinstance(lay,int):
        if lay==2: K_Deq = 3.46
    else:
        K_Deq[lay == 2] = 3.46
    ltp = rp * dte
    Deq = (K_Deq * ltp ** 2) / (pi * dte) - dte
    hs = Nus * ks / Deq
    return hs

#endregion