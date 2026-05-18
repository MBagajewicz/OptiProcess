#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion

# region Import Library
from math import sqrt, pi
import numpy as np
#endregion


#region Calculations
def Kettle_counting_table(Ds, dte, Npt, rp, lay):
    # Counting table
    KNPt = sqrt(0.9) * np.ones(Npt.shape)
    if isinstance(Npt,float) or isinstance(Npt,int):
        if Npt==1: KNPt = sqrt(0.93)
    else:
        KNPt[Npt == 1] = sqrt(0.93)
    Db = Ds*KNPt
    ltp = rp*dte
    Klay = np.ones(lay.shape)
    Klay[lay == 2] = 0.866
    Ntt = np.round((pi*Db**2)/(4*ltp**2*Klay))
    return Ntt
#endregion