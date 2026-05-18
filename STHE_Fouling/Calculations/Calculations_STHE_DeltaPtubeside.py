#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello             Proposed
#   0.2          28-Feb-2025     Mariana Mello             Add options of Tube Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p']
#   0.4          02-Jul-2025     Augusto Vieira            Included fouling thickness dependency
##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_Reynolds_tubeside, Calculations_STHE_velocity_tubeside, Calculations_STHE_frictionfactor
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

def STHE_tubeside_DeltaP(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, L, m_p,ft_thk):
    # Tube-side pressure drop
    if m_p['Tube_Method'] == 'Dewiit_Saunders' or 'Gnieliski' or 'Hausen' or 'Sieder_Tate':
        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
        ft = Calculations_STHE_frictionfactor.STHE_tubeside_frictionfactor(mt, rot, mit, Ds, dte, Npt, rp, lay, thk, m_p,ft_thk)
        K = 1.6 * np.ones(Npt.shape)
        K[Npt == 1] = 0.9
        dti = dte - 2 * thk
        df = dti-2*ft_thk
        DPt = (rot * ft * Npt * L * vt ** 2) / (2 * df) + rot * K * Npt * vt ** 2 / 2

    elif m_p['Tube_Method'] == "Dittus_Boelter":
        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
        Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
        ft = 0.014 + 1.056 / (Ret**0.42)
        K = 1.6 * np.ones(Npt.shape)
        if isinstance(Npt, float) or isinstance(Npt, int):
            if Npt == 1: K = 0.9
        else:
              K[Npt == 1] = 0.9
        dti = dte - 2 * thk
        df = dti-2*ft_thk
        DPt = (rot * ft * Npt * L * vt**2) / (2 * df) + rot * K * Npt * (vt**2) / 2

    else:
        raise ValueError(f"Invalid Tube Method: {m_p['Tube_Method']}.")

    return DPt

#endregion
