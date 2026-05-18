#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion


#region Import Library
from Kettle.Calculations import Calculations_Kettle_Reynolds_shellside
#endregion

#region Calculations
def Kettle_Nusselt_shellside(ms, ros, Cps, mis, ks, Ds, dte, rp, lay, L, Nb):
    # Shell-side Nusselt number
    Res = Calculations_Kettle_Reynolds_shellside.Kettle_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb)
    Prs = Cps * mis / ks
    Nus = 0.36 * Res**0.55 * Prs**(1/3)
    return Nus

#endregion
