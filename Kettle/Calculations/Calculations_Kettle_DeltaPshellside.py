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
from Kettle.Calculations import Calculations_Kettle_Reynolds_shellside, Calculations_Kettle_velocity_shellside
from math import pi
import numpy as np
#endregion

#region Calculations
def Kettle_shellside_DeltaP(ms, ros, mis, Ds, dte, rp, lay, L, Nb):
    # Shell-side pressure drop
    K_Deq = 4 * np.ones(lay.shape)
    if isinstance(lay,float) or isinstance(lay,int):
        if lay==2: K_Deq = 3.46
    else:
        K_Deq[lay == 2] = 3.46
    ltp = rp * dte
    Deq = (K_Deq * ltp**2) / (pi * dte) - dte
    vs = Calculations_Kettle_velocity_shellside.Kettle_shellside_velocity(ms, ros, Ds, rp, L, Nb)
    Res = Calculations_Kettle_Reynolds_shellside.Kettle_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb)
    fs = 1.728 / Res**0.188
    DPs = (ros * fs * Ds * (Nb + 1) * vs**2) / (2 * Deq)
    return DPs

#endregion