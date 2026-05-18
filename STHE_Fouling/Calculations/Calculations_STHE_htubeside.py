#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original
#   0.2          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.3          02-Jul-2025     Augusto Vieira            Included fouling thickness dependency

##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_Nusselt_tubeside
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

def STHE_h_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay, L, m_p,ft_thk):
    Nut = Calculations_STHE_Nusselt_tubeside.STHE_Nusselt_tubeside(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp,
                                                                   lay, L, m_p,ft_thk)
    dti = dte - 2 * thk
    df = dti-2*ft_thk
    ht = Nut * kt / df

    #print('ht',ht)
    return ht

#endregion
