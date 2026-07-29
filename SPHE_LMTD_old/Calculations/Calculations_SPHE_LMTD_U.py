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
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_h,Calculations_SPHE_LMTD_area
import numpy as np
#endregion

#region Calculations

def SPHE_overall_coefficient(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc, Rfh, Rfc, kplate):
    # Overall heat transfer coefficient
    
    hh, hc = Calculations_SPHE_LMTD_h.SPHE_h(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc)
    #_, hc = Calculations_SPHE_LMTD_h.SPHE_h(L, dh, dc, ds, H, thk, mh, mc, mih, mic, Cph, Cpc, kh, kc)

    U = 1 / (1 / hh + Rfh + (thk / kplate) + 1 / hc + Rfc)
    
    return U


def SPHE_overall_coefficient_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate):
    # Overall heat transfer coefficient
    hhub, hcub = Calculations_SPHE_LMTD_h.SPHE_h_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax)
    #_, hcub = Calculations_SPHE_LMTD_h.SPHE_h_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax)

    Uub = 1 / (1 / hhub + Rfh  + (thk / kplate) + 1 / hcub + Rfc)

    return Uub


def SPHE_Qspec(mh, Thtarget, Thi, Cph):

    Qspec = mh * (Thi-Thtarget) * Cph

    return Qspec




#def SPHE_LMTDub(.........):




def SPHE_Qub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate):

    Uub = SPHE_overall_coefficient_ub(L, dh, dc, ds, H, thk, mh, mc, mimin, Cpmax, kmax, Rfh, Rfc, kplate)
    A = Calculations_SPHE_LMTD_area.SPHE_area(L, H)
    #LMTDub = Calculations_SPHE_LMTD_U.SPHE_LMTDub(.........)
    LMTDub = 100
    Qub = Uub * A * LMTDub

    return Qub
#endregion