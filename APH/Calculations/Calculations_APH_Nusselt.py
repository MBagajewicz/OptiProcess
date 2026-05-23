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
from APH.Calculations import Calculations_APH_Prandtl, Calculations_APH_Reynolds
import numpy as np
#endregion


#region Calculations

def APH_Nu_air(Nr, Do, rpv, lf, rph, L,  m_air, rho_air, mu_air, Cp_air, k_air):
    # air side Nusselt
    Re_air = Calculations_APH_Reynolds.APH_Re_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air)
    Pr_air = Calculations_APH_Prandtl.APH_Pr_air(Cp_air, mu_air, k_air)
    Nu_air = 0.36 * np.power(Re_air,0.55) * np.power(Pr_air, 0.33)

    return Nu_air

def APH_Nu_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, Cp_gas, k_gas):
    # tube side Nusselt
    Re_tube = Calculations_APH_Reynolds.APH_Re_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas)
    Pr_tube = Calculations_APH_Prandtl.APH_Pr_tube(Cp_gas, mu_gas, k_gas)

    Nu_tube = 0.023 * np.power(Re_tube, 0.8) * np.power(Pr_tube, 0.4)
    return Nu_tube


#endregion
