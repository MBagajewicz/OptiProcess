#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from Airpreheater.Calculations import Calculations_Airpreheater_hc, Calculations_Airpreheater_hh
#endregion

#region Calculations

def Airpreheater_overall_coefficient(Ntp, Lp, Lw, Npc, Sa, Nph, Rfh, Rfc, thk, kplate, bp, phi, Cpc, Cph, mic, mih, kc, kh, roc, roh, mc, mh):
    # Overall heat transfer coefficient
    hc = Calculations_Airpreheater_hc.Airpreheater_hc(Ntp, Lw, Npc, Sa, bp, phi, kc, Cpc, mic, roc, mc)
    hh = Calculations_Airpreheater_hh.Airpreheater_hh(Ntp, Lp, Lw, Nph, Sa, bp, phi, kh, Cph, mih, roh, mh)
    U = 1/(1/hh + Rfh + Rfc + thk / kplate + 1/hc)
    return U

#endregion