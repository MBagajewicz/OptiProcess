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
from Kettle.Calculations import Calculations_Kettle_hshellside, Calculations_Kettle_htubeside
import numpy as np
#endregion

#region Calculations

def Kettle_overall_coefficient(mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb):
    # Overall heat transfer coefficient
    dti = dte - 2*thk
    ht = Calculations_Kettle_htubeside.Kettle_h_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay)
    hs = Calculations_Kettle_hshellside.Kettle_h_shellside(ms, ros, Cps, mis, ks, Ds, dte, rp, lay, L, Nb)
    U = 1 / (1/ht*(dte/dti) + Rft*(dte/dti) + dte * np.log(dte/dti) / 2 / ktube + Rfs + 1/hs)
    return U

#endregion