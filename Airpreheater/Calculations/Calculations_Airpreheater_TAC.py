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
from Airpreheater.Calculations import Calculations_Airpreheater_area, Calculations_Airpreheater_DeltaP_channel, Calculations_Airpreheater_DeltaP_port
#endregion

#region Calculations

def Airpreheater_TAC(int_rate, n, Ntp, Lp, Lw, par_a, par_b, Dp, Nph, Npc, Sa, Nop, pc, eta, phi, bp, mh, mc, roh, roc, mih, mic):
    r = ((int_rate*(1+int_rate)**n)) / (((1+int_rate)**n) - 1)
    Atot = Calculations_Airpreheater_area.Airpreheater_area(phi, Ntp, Lp, Lw)
    Cap = par_a*Atot**par_b   # Capital cost
    deltaPtoth = (Calculations_Airpreheater_DeltaP_channel.Airpreheater_DeltaP_channel(Ntp, Lp, Lw, Dp, Nph, Sa, bp, phi, roh, mih, mh) +
                  Calculations_Airpreheater_DeltaP_port.Airpreheater_DeltaP_port(Dp, Nph, mh, roh))*100000
    deltaPtotc = (Calculations_Airpreheater_DeltaP_channel.Airpreheater_DeltaP_channel(Ntp, Lp, Lw, Dp, Npc, Sa, bp, phi, roc, mic, mc) +
                  Calculations_Airpreheater_DeltaP_port.Airpreheater_DeltaP_port(Dp, Npc, mc, roc))*100000
    Cop_h = Nop*(pc/1000)*((deltaPtoth*mh)/(eta*roh)) # Operating cost on a yearly fot the hot stream
    Cop_c = Nop*(pc/1000)*((deltaPtotc*mc)/(eta*roc)) # Operating cost on a yearly fot the cold stream
    TAC = r*Cap + Cop_h + Cop_c
    return TAC

#endregion