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
from Kettle.Calculations import Calculations_Kettle_velocity_tubeside
#endregion

#region Calculations

def Kettle_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay):
    # Tube-side Reynolds number
    vt = Calculations_Kettle_velocity_tubeside.Kettle_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay)
    dti = dte - 2 * thk
    Ret = (dti * vt * rot) / mit
    return Ret

#endregion
