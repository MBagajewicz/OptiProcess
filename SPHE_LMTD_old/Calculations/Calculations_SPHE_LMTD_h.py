#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
#################################################################################################################
#endregion


#region Import Library
from math import pi
import numpy as np
#endregion
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_Reynolds
#region Calculations

def SPHE_h(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc):
    
    Dh = 2 * (dh ) * (H ) / ((dh + H) )  # the hydraulic diameter of hot side  (ft)
    Dc = 2 * (dc ) * (H ) / ((dc + H) )  # the hydraulic diameter of cold side  (ft)
    Ds = (1.28 * (L ) * ((dh + dc + 2 * thk) ) + ((ds ) ** 2)) ** 0.5  # the spiral outer diameter (ft)
    Gh = (mh ) / ((dh ) * (H ))  # The mass flux of hot side    lb/(h*ft2)
    Gc = (mc ) / ((dc ) * (H ))  # The mass flux of cold side   lb/(h*ft2)
    Prh = (mih * Cph / kh)
    Prc = (mic * Cpc / kc)

    Reh, _, _, _ = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, mh, mc, mih, mic, L, thk, ds)
    _, Rec, _, _ = Calculations_SPHE_LMTD_Reynolds.SPHE_Reynolds(dh, dc, H, mh, mc, mih, mic, L, thk, ds)

    hh = (1 + 3.54 * Dh / Ds) * 0.023 * (Cph) * Gh * (Reh ** (-0.2)) * (Prh ** (-2 / 3)) # Btu/(sq ft * hr * F) 湍流!!!!!!!!!
    hc = (1 + 3.54 * Dc / Ds) * 0.023 * (Cpc) * Gc * (Rec ** (-0.2)) * (Prc ** (-2 / 3)) #

    return hh, hc

def SPHE_h_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax):

    Dh = 2 * (dh) * (H) / ((dh + H) )  # the hydraulic diameter of hot side  (ft)
    Dc = 2 * (dc) * (H) / ((dc + H) )  # the hydraulic diameter of cold side  (ft)
    Ds = (1.28 * (L) * ((dh + dc + 2 * thk) / 0.3048) + ((ds / 0.3048) ** 2)) ** 0.5  # the spiral outer diameter (ft)
    Gh = (mh ) / ((dh) * (H))  # The mass flux of hot side    lb/(h*ft2)
    Gc = (mc ) / ((dc) * (H))  # The mass flux of cold side   lb/(h*ft2)

    hhub = (1 + 3.54 * Dh / Ds) * 0.023 *  (Gh**0.8)* (Dh**(-0.2)) * (Cpmax ** (1/3)) * (mimin ** (-7 / 15)) * (kmax ** (2/3))# Btu/(sq ft * hr * F) 湍流!!!!!!!!!
    hcub = (1 + 3.54 * Dc / Ds) * 0.023 *  (Gc**0.8)* (Dc**(-0.2)) * (Cpmax ** (1/3)) * (mimin ** (-7 / 15)) * (kmax ** (2/3)) #

    return hhub, hcub
#endregion