#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Proposed
#   0.2          27-Feb-2025     Mariana Mello             Add options of Tube Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.4          02-Jul-2025     Augusto Vieira            Included fouling thickness dependency

##################################################################################################################
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

#region Import Library
from STHE.Calculations import Calculations_STHE_velocity_tubeside
#endregion

#region Calculations

def STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk):
    # Tube-side Reynolds number
    if m_p['Tube_Method'] == 'Dewiit_Saunders' or 'Gnieliski' or 'Hausen' or 'Sieder_Tate':
        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
        dti = dte - 2 * thk
        df = dti - 2 * ft_thk
        Ret = (df * vt * rot) / mit

    elif m_p['Tube_Method'] == "Dittus_Boelter":

        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
        dti = dte - 2 * thk
        df = dti - 2 * ft_thk
        Ret = (df * vt * rot) / mit

    else:
        raise ValueError(f"Invalid Tube Method: {m_p['Tube_Method']}.")

    return Ret

#endregion

