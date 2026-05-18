#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello             Proposed
#   0.2          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.3          02-Jul-2025     Augusto Vieira            Included fouling thickness dependency

##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_hshellside, Calculations_STHE_htubeside
import numpy as np
#endregion

##################################################################################################################


# region Notes for Last Update


"""
Notes for last update:
- ft_thk fouling thickness dependency is included
- df is fouled diameter

"""

# endregion
##################################################################################################################


#region Calculations

def STHE_overall_coefficient(mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p,ft_thk):
    # Overall heat transfer coefficient
    dti = dte - 2*thk
    df = dti-2*ft_thk
    ht = Calculations_STHE_htubeside.STHE_h_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay, L, m_p,ft_thk)
    hs = Calculations_STHE_hshellside.STHE_h_shellside(ms, ros, Cps, mis, ks, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    U = 1 / (1/ht*(dte/df) + Rft*(dte/df) + dte * np.log(dte/dti) / 2 / ktube + Rfs + 1/hs)
    return U

#endregion
