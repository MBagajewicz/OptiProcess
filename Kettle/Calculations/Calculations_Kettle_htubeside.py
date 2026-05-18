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
from Kettle.Calculations import Calculations_Kettle_Nusselt_tubeside
#endregion

#region Calculations

def Kettle_h_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay):
    Nut = Calculations_Kettle_Nusselt_tubeside.Kettle_Nusselt_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay)
    dti = dte - 2 * thk
    ht = Nut * kt / dti
    return ht

#endregion