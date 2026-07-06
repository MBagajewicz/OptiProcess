#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Use SPHE_DT namespace consistently
###################################################################################################################
#endregion

#region Import Library
import numpy as np
from math import pi
from SPHE_DT.Calculations import Calculations_SPHE_DT_U
#endregion

#region Calculations

def SPHE_correction_factor(L, H, dh, dc, ds, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate):
    """Calculate the LMTD correction factor used by the length-based SPHE model."""
    A = 2 * H * L
    Ac = H * dc

    U = Calculations_SPHE_DT_U.SPHE_overall_coefficient(
        L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate
    )
    NTUh = U * A / (mh * Cph)
    NTUc = U * A / (mc * Cpc)
    CN = 2 * ((NTUh * NTUc * pi * Ac / A) ** 0.5)
    return np.log(1 + CN**2) / (CN**2)

#endregion
