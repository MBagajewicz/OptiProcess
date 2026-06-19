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
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_velocity
from math import pi
import numpy as np
#endregion

#region Calculations

def SPHE_Reynolds(dh, dc, H, mh, mc, mih, mic, L, thk, ds):
    # Shell-side Reynolds number
    
    Ds = np.sqrt(1.28 * (L) * ((dh + dc + 2 * thk) ) + ((ds ) ** 2))  # the spiral outer diameter (ft)
    Dh = 2 * (dh ) * (H ) / ((dh + H) )  # the hydraulic diameter of hot side  (ft)
    Dc = 2 * (dc ) * (H ) / ((dc + H) )  # the hydraulic diameter of cold side  (ft)
    Gh = (mh ) / ((dh ) * (H ))  # The mass flux of hot side    lb/(h*ft2)
    Gc = (mc ) / ((dc ) * (H ))  # The mass flux of cold side   lb/(h*ft2)

    Reh = Dh * Gh / (mih )
    Rec = Dc * Gc / (mic )
    Reeh = 20000 * ((Dh / Ds) ** 0.32)
    Reec = 20000 * ((Dc / Ds) ** 0.32)
    
    return Reh, Rec, Reeh, Reec

def SPHE_Reynolds_ub(dh, dc, H, mh, mc, mimin, L, thk, ds):

    Ds = (1.28 * (L ) * ((dh + dc + 2 * thk) ) + ((ds ) ** 2)) ** 0.5  # the spiral outer diameter (ft)
    Dh = 2 * (dh ) * (H ) / ((dh + H) )  # the hydraulic diameter of hot side  (ft)
    Dc = 2 * (dc ) * (H ) / ((dc + H) )  # the hydraulic diameter of cold side  (ft)
    Gh = (mh ) / ((dh ) * (H ))  # The mass flux of hot side    lb/(h*ft2)
    Gc = (mc ) / ((dc ) * (H ))  # The mass flux of cold side   lb/(h*ft2)

    Rehub = Dh * Gh / (mimin )
    Recub = Dc * Gc / (mimin )
    Reeh = 20000 * ((Dh / Ds) ** 0.32)
    Reec = 20000 * ((Dc / Ds) ** 0.32)

    return Rehub, Recub, Reeh, Reec
#endregion
