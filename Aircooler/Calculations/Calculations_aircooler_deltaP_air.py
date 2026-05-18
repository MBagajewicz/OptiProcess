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
    Calculations_aircooler_velocity_coldstream,
    Calculations_aircooler_prop_roc,
    Calculations_aircooler_ltp,
    Calculations_aircooler_Re_coldstream,
    Calculations_aircooler_sf
)
import numpy as np
#endregion

#region Calculations

def aircooler_deltaP_air(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr, mh, Cph, Thi, Tho):
    # Gc - air mass flux
    vcmax = Calculations_aircooler_velocity_coldstream.aircooler_velocity_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf,
                                                                                     Lf, tf, mh, Cph, Thi, Tho, Tco, Tci)
    roc = Calculations_aircooler_prop_roc.aircooler_calc_prop_air_roc(Tco, Tci)
    Gc = roc*vcmax
    # fc - friction factor
    ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    Df = Dte + 2*Lf
    a = (ltp - Df)/Dte
    #a = (rp - Df)/Dte
    Rec = Calculations_aircooler_Re_coldstream.aircooler_Reynolds_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf,
                                                                             mh, Cph, Thi, Tho, Tco, Tci)
    sf = Calculations_aircooler_sf.aircooler_sf(Nf, tf)
    Reeff = Rec*(sf/Lf)
    fc = (1+(2*np.exp(-a/4))/(1+a))*(0.021 + (27.2/Reeff) + (0.29/(Reeff**0.2)))
    # DeltaP_c - air-side pressure drop
    dPc = 1.1*((2*fc*(Gc**2)*Nr)/roc)
    return dPc

#endregion