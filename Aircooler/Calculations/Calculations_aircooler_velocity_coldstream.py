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
    Calculations_aircooler_ltp,
    Calculations_aircooler_mc,
    Calculations_aircooler_prop_roc
)
#endregion

#region Calculations

def aircooler_velocity_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho, Tco, Tci):
    mc = Calculations_aircooler_mc.aircooler_mc(mh, Cph, Thi, Tho, Tco, Tci)
    roc = Calculations_aircooler_prop_roc.aircooler_calc_prop_air_roc(Tco, Tci)
    # Velocity of the air stream through the minimum flow area
    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    # W = bundle width
    W = Ltp*Ntr
    # Aface = total projection area of the air cooler
    Aface = Nbay*Nbbay*W*L
    # FAR = free area ratio
    FAR = 1 - ((Dte+(2*Nf*Lf*tf))/Ltp)
    vcmax = (mc/roc)/(Aface*FAR)
    return vcmax

#endregion
