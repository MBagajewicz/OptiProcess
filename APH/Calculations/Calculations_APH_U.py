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
from APH.Calculations import Calculations_APH_tube, Calculations_APH_convection_coefficient
import numpy as np
#endregion


#region Calculations

def APH_U(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, Cp_gas, k_gas, rpv, lf, rph, L, m_air, rho_air, mu_air, Cp_air, k_air, Rf_gas, Rf_air):
    # overall heat transfer coefficient
    h_tube = Calculations_APH_convection_coefficient.APH_h_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, Cp_gas, k_gas)
    h_air = Calculations_APH_convection_coefficient.APH_h_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air, Cp_air, k_air)
    Di = Calculations_APH_tube.APH_Di(Do, td)
    
    U = 1/((1/h_tube + Rf_gas)*(Do/Di) + (Do/(2*k_gas)) * np.log(Do/Di) + (1/h_air + Rf_air))
    return U

#endregion
