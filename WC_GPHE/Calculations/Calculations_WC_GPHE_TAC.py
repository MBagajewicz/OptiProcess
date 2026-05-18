#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          07-Feb-2024     Mariana Mello             Proposed
#   0.2          24-Sep-2025     Mariana Mello             Update to fix error
##################################################################################################################
#endregion


#region Import Library
from GPHE.Calculations import Calculations_GPHE_DeltaP_channel, Calculations_GPHE_DeltaP_port, Calculations_GPHE_area
#endregion

#region Calculations

def WC_GPHE_TAC(Fw, Ntp, Lp, Lw, Dp, Npc, Sa, bp, phi, roc, mic, pcw, pc, eta, Nop, cf, cv, alpha, int_rate, n, Nph, mh, roh, mih):
    deltaPtotc = (Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Npc, Sa, bp, phi, roc, mic, Fw) +
                  Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Npc, Fw, roc)) * 100000
    #print('DPc', deltaPtotc)
    deltaPtoth = (Calculations_GPHE_DeltaP_channel.GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Nph, Sa, bp, phi, roh, mih, mh) +
                  Calculations_GPHE_DeltaP_port.GPHE_DeltaP_port(Dp, Nph, mh, roh)) * 100000

    Cop_h = ((mh/roh) * ((deltaPtoth/1000)/eta))
    Cop_w = ((Fw/roc) * ((deltaPtotc/1000)/eta))

    OPEX = Nop * (pcw*Fw*3600 + pc*(Cop_h + Cop_w))
    #OPEX = Nop*(3600*pcw*Fw + pc*(((Fw/roc)*deltaPtotc)/eta))
    ##OPEX = pcw*Fw + pc*(Fw/roc)*deltaPtotc/eta*Nop

    A = Calculations_GPHE_area.GPHE_area(phi, Ntp, Lp, Lw)
    CAPEX = cf + cv*(A**alpha)
    af = ((int_rate * (1 + int_rate)**n))/(((1 + int_rate)**n) - 1)

    TAC = OPEX + af*CAPEX
    return TAC

#endregion