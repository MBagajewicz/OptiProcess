#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
###################################################################################################################
#endregion

# region Import Library
from math import log, sqrt
import numpy as np
from math import pi
#endregion
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_U

#region Calculations

def SPHE_correction_factor(L, H, dh, dc, ds, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate):
    # LMTD correction factor

    A = 2 * H * L  # The heat exchanger area (2)
    Ac = H  * dc 

    U = Calculations_SPHE_LMTD_U.SPHE_overall_coefficient(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate)
    NTUh = U * A / (mh  * Cph )
    NTUc = U * A / (mc  * Cpc )
    CN = 2 * ((NTUh * NTUc * pi * Ac / A) ** 0.5)
    F = (np.log(1 + CN ** 2)) / (CN**2)

    return F

#endregion