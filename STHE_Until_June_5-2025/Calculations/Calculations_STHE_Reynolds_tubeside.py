#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Proposed
#   0.2          27-Feb-2025     Mariana Mello             Add options of Tube Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_velocity_tubeside
#endregion

#region Calculations

def STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p):
    # Tube-side Reynolds number
    if m_p['Tube_Method'] == 'Dewiit_Saunders' or 'Gnieliski' or 'Hausen' or 'Sieder_Tate':
        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p)
        # Diâmetros interno (dti) e de depósito (df)
        dti = dte - 2 * thk
        #df = dti - 2 * ft_thk
        # Number of Reynolds
        #Ret = (df * vt * rot) / mit
        Ret = (dti * vt * rot) / mit

    elif m_p['Tube_Method'] == "Dittus_Boelter":
        vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p)
        dti = dte - 2 * thk
        Ret = (dti * vt * rot) / mit

    else:
        raise ValueError(f"Invalid Tube Method: {m_p['Tube_Method']}.")

    return Ret

#endregion

