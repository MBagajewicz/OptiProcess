#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Sep-2025     Sung Young Kim            original
##################################################################################################################
#endregion

#region Import Library
from APH.Calculations import Calculations_APH_area, Calculations_APH_tube
#endregion


#region Calculations

def APH_v_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air):
    # air side velocity
    Ar = Calculations_APH_area.APH_Ar(Nr, Do, rpv, lf, rph, L)

    v_air = m_air /(rho_air * Ar)
    return v_air


def APH_v_tube(Do, td, Nc, Nr, m_gas, rho_gas):
    # tube side velocity
    A1 = Calculations_APH_area.APH_A1(Do, td)
    Nt = Calculations_APH_tube.APH_Nt(Nc, Nr)

    v_tube = m_gas/(rho_gas * A1 * Nt)
    return v_tube


#endregion
