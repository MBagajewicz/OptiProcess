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
from Kettle.Calculations import Calculations_Kettle_Reynolds_tubeside
#endregion

#region Calculations

def Kettle_Nusselt_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay):
    # Tube-side Nusselt number
    Ret = Calculations_Kettle_Reynolds_tubeside.Kettle_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay)
    Prt = Cpt * mit / kt
    if yfluid == 1:
        n = 0.4
    else:
        n = 0.3
    Nut = 0.023 * Ret**0.8 * Prt**n
    return Nut

#endregion
