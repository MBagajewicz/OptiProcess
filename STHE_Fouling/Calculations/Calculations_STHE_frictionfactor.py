#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello             Proposed
#   0.2          28-Feb-2025     Mariana Mello             Add options of Shell Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.4          02-Jul-2025     Augusto Vieira            Included fouling thickness dependency

##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_Reynolds_tubeside
#endregion

##################################################################################################################


# region Notes for Last Update


"""
Notes for last update:
- ft_thk fouling thickness dependency is included

"""

# endregion
##################################################################################################################


#region Calculations

def STHE_tubeside_frictionfactor(mt, rot, mit, Ds, dte, Npt, rp, lay, thk, m_p,ft_thk):
    # Tube-side friction factor
    # Reynold number
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
    ft = 64 / Ret
    ft[Ret > 1311] = 0.048
    ft[Ret > 3380] = 0.014 + 1.056/(Ret[Ret > 3380]**0.42)

    return ft

# endregion

