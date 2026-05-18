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
from Airpreheater.Calculations import Calculations_Airpreheater_Nusselt
#endregion

#region Calculations

def Airpreheater_hc(Ntp, Lw, Npc, Sa, bp, phi, kc, Cpc, mic, roc, mc):
    Deq = 2 * bp / phi
    Nuc = Calculations_Airpreheater_Nusselt.Airpreheater_Nusselt(Ntp, Lw, Npc, Sa, Cpc, mic, kc, bp, phi, roc, mc)
    hc = kc * Nuc / Deq
    return hc

#endregion