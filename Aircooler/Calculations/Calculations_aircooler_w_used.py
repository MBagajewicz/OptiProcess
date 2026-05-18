#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Import Library
from Aircooler.Calculations import Calculations_aircooler_deltaP_fan, Calculations_aircooler_mc, Calculations_aircooler_prop_rocout
#endregion

#region Calculations

def aircooler_w_used(mh, Cph, Thi, Tho, Nbay, Nfanbay, Dfan, rp, Ntr, Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr, etafan, etasr,
                     etamotor):
    # W_used - power consumption per fan
    dPfan = Calculations_aircooler_deltaP_fan.aircooler_deltaP_fan(mh, Cph, Thi, Tho, Nbay, Nfanbay, Dfan, rp, Ntr,
                                                                   Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr)
    mc = Calculations_aircooler_mc.aircooler_mc(mh, Cph, Thi, Tho, Tco, Tci)
    rocout = Calculations_aircooler_prop_rocout.aircooler_calc_rocout(Tco)
    qfan = (mc/rocout)/(Nbay*Nfanbay)
    wused = (dPfan*qfan)/(1000*etafan*etasr*etamotor)
    return wused

#endregion
