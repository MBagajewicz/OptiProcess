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
from Aircooler.Calculations import (
        Calculations_aircooler_prop_roc,
        Calculations_aircooler_deltaP_air,
        Calculations_aircooler_prop_rocout,
        Calculations_aircooler_mc)
from math import pi
#endregion

#region Calculations

def aircooler_deltaP_fan(mh, Cph, Thi, Tho, Nbay, Nfanbay, Dfan,rp, Ntr, Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr):
    roc = Calculations_aircooler_prop_roc.aircooler_calc_prop_air_roc(Tco, Tci)
    mc = Calculations_aircooler_mc.aircooler_mc(mh, Cph, Thi, Tho, Tco, Tci)
    rocout = Calculations_aircooler_prop_rocout.aircooler_calc_rocout(Tco)
    # Fan power consumption
    # qfan - air volumetric flow rate per fan
    qfan = (mc / rocout) / (Nbay*Nfanbay)

    # vfr - air velocity through the fans
    vfr = qfan / ((pi/4)*(Dfan**2))

    # Lfanp - distance between the fan centers
    Lfanp = 1.1*Dfan

    # dPfan - total air-side pressure variation
    dPc = Calculations_aircooler_deltaP_air.aircooler_deltaP_air(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr,
                                                                 mh, Cph, Thi, Tho)
    dPfan = dPc + (roc*(vfr**2))/2
    #print('dPfan', dPfan)

    return dPfan

#endregion
