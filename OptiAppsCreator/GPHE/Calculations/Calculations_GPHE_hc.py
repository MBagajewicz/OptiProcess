#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from GPHE.Calculations import Calculations_GPHE_Nusselt
#endregion

#region Calculations

def GPHE_hc(Ntp, Lw, Npc, Sa, bp, phi, kc, Cpc, mic, roc, mc):
    Deq = 2 * bp / phi
    Nuc = Calculations_GPHE_Nusselt.GPHE_Nusselt(Ntp, Lw, Npc, Sa, Cpc, mic, kc, bp, phi, roc, mc)
    hc = kc * Nuc / Deq
    return hc

#endregion