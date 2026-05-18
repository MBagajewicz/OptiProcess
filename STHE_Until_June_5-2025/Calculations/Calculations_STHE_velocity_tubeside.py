#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello              Proposed
#   0.2          27-Feb-2025     Mariana Mello             Add options of Tube Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import Calculations_STHE_countingtable
from math import pi
#endregion

#region Calculations

def STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p):
    # Tube-side velocity
    if m_p['Tube_Method'] == "Dewiit_Saunders" or 'Gnieliski' or 'Hausen' or 'Sieder_Tate':
        qt = mt/rot
        # Diâmetros interno (dti) e de depósito (df)
        dti = dte - 2 * thk
        #df = dti - 2 * ft_thk
        Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, dte, Npt, rp, lay, m_p)
        Ntp = Ntt / Npt
        #vt = (qt / Ntp) / (pi * df ** 2 / 4)
        vt = (qt / Ntp) / (pi * dti ** 2 / 4)

    elif m_p['Tube_Method'] == "Dittus_Boelter":
        qt = mt / rot
        dti = dte - 2 * thk
        Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, dte, Npt, rp, lay, m_p)
        Ntp = Ntt / Npt
        vt = (qt / Ntp) / (pi * dti ** 2 / 4)

    else:
        raise ValueError(f"Invalid Tube Method: {m_p['Tube_Method']}.")

    return vt

#endregion


