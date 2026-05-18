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

def Airpreheater_hh(Ntp, Lp, Lw, Nph, Sa, bp, phi, kh, Cph, mih, roh, mh):
    Deq = 2*bp/phi
    Nuh = Calculations_Airpreheater_Nusselt.Airpreheater_Nusselt(Ntp, Lw, Nph, Sa, Cph, mih, kh, bp, phi, roh, mh)
    hh = kh * Nuh / Deq
    return hh

#endregion