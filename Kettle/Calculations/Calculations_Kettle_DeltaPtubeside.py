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
from Kettle.Calculations import Calculations_Kettle_Reynolds_tubeside, Calculations_Kettle_velocity_tubeside
from math import pi
import numpy as np
#endregion

#region Calculations

def Kettle_tubeside_DeltaP(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, L):
    # Tube-side pressure drop
    vt = Calculations_Kettle_velocity_tubeside.Kettle_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay)
    Ret = Calculations_Kettle_Reynolds_tubeside.Kettle_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay)
    ft = 0.014 + 1.056 / Ret ** 0.42
    K = 1.6 * np.ones(Npt.shape)
    if isinstance(Npt,float) or isinstance(Npt,int):
        if Npt == 1: K = 0.9
    else:
        K[Npt == 1] = 0.9
    dti = dte - 2 * thk
    DPt = (rot * ft * Npt * L * vt ** 2) / (2 * dti) + rot * K * Npt * vt ** 2 / 2
    return DPt

#endregion