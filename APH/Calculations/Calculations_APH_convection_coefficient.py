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
from APH.Calculations import Calculations_APH_Nusselt, Calculations_APH_tube
import numpy as np
#endregion


#region Calculations

def APH_h_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air, Cp_air, k_air):
    # air side convection coefficient
    Nu_air = Calculations_APH_Nusselt.APH_Nu_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air, Cp_air, k_air)
    h_air = Nu_air * k_air / Do
    return h_air

def APH_h_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, Cp_gas, k_gas):
    # tube side convection coefficient
    Di = Calculations_APH_tube.APH_Di(Do, td)
    Nu_tube = Calculations_APH_Nusselt.APH_Nu_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, Cp_gas, k_gas)
    h_tube = Nu_tube * k_gas/Di
    return h_tube
#endregion
