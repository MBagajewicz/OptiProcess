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
    Calculations_aircooler_prop_mic,
    Calculations_aircooler_prop_roc,
    Calculations_aircooler_velocity_coldstream
)
#endregion

#region Calculations

def aircooler_Reynolds_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho, Tco, Tci):
    mic = Calculations_aircooler_prop_mic.aircooler_calc_prop_air_mic(Tco, Tci)
    roc = Calculations_aircooler_prop_roc.aircooler_calc_prop_air_roc(Tco, Tci)
    # Reynolds number of cold stream
    vcmax = Calculations_aircooler_velocity_coldstream.aircooler_velocity_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf,
                                                                                     Lf, tf, mh, Cph, Thi, Tho, Tco,
                                                                                     Tci)
    Rec = (Dte*vcmax*roc)/mic
    return Rec

#endregion