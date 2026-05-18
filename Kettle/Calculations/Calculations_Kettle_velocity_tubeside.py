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
from Kettle.Calculations import Calculations_Kettle_countingtable
from math import pi
#endregion

#region Calculations

def Kettle_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay):
    # Tube-side velocity
    qt = mt / rot
    dti = dte - 2 * thk
    Ntt = Calculations_Kettle_countingtable.Kettle_counting_table(Ds, dte, Npt, rp, lay)
    Ntp = Ntt / Npt
    vt = (qt / Ntp) / (pi * dti ** 2 / 4)
    return vt

#endregion