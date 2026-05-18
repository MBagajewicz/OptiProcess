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
from math import pi
from Aircooler.Calculations import (
    Calculations_aircooler_prop_mic,
    Calculations_aircooler_prop_kc,
    Calculations_aircooler_prop_cpc,
    Calculations_aircooler_Re_coldstream,
    Calculations_aircooler_Ar,
    Calculations_aircooler_Aot
)
#endregion


#region Calculations

def aircooler_Nusselt_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho, Tco, Tci):
    mic = Calculations_aircooler_prop_mic.aircooler_calc_prop_air_mic(Tco, Tci)
    kc = Calculations_aircooler_prop_kc.aircooler_calc_prop_air_kc(Tco, Tci)
    Cpc = Calculations_aircooler_prop_cpc.aircooler_calc_prop_air_Cpc(Tco, Tci)
    # Nusselt number of cold stream
    Rec = Calculations_aircooler_Re_coldstream.aircooler_Reynolds_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf,
                                                                             mh, Cph, Thi, Tho, Tco, Tci)
    Prc = (Cpc*mic) / kc
    # Df = fin diameter
    Df = Dte + 2*Lf
    # Ar = outside bare area per unit length
    Ar = Calculations_aircooler_Ar.aircooler_Ar(Dte)
    # Aot = the total finned surface area per unit length
    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    ratio_Aot_Ar = Aot/Ar
    # Nusselt number
    Nuc = 0.38*(Rec**0.6)*(Prc**(1/3))*(ratio_Aot_Ar**(-0.15))
    return Nuc

#endregion