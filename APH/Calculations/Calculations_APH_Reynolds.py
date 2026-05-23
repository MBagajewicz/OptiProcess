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
from APH.Calculations import Calculations_APH_velocity, Calculations_APH_tube
#endregion


#region Calculations

def APH_Re_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air):
    # air side Reynolds number
    v_air = Calculations_APH_velocity.APH_v_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air)

    Re_air = rho_air * v_air * Do / mu_air
    return Re_air

def APH_Re_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas):
    # tube side Reynolds number
    v_tube = Calculations_APH_velocity.APH_v_tube(Do, td, Nc, Nr, m_gas, rho_gas)
    Di = Calculations_APH_tube.APH_Di(Do, td)

    Re_tube = rho_gas * v_tube * Di / mu_gas
    return Re_tube

#endregion
