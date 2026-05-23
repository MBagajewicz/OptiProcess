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
import numpy as np
from APH.Calculations import Calculations_APH_friction_factor, Calculations_APH_tube, Calculations_APH_boxsize, Calculations_APH_velocity
#endregion


#region Calculations

def APH_DeltaP_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air):
    # air side pressure drop
    Dhyd = Calculations_APH_tube.APH_Dhyd(Do, rph)
    f_air = Calculations_APH_friction_factor.APH_f_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air)
    L_eff = Calculations_APH_boxsize.APH_L_eff(Nr, rpv, Do)
    v_air = Calculations_APH_velocity.APH_v_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air)

    DeltaP_air = rho_air * f_air * L_eff * np.power(v_air, 2)/(2*Dhyd)
    return DeltaP_air

def APH_DeltaP_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, L):
    # tube side pressure drop
    K = 0.9 # for one pass
    f_tube = Calculations_APH_friction_factor.APH_f_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas)
    v_tube = Calculations_APH_velocity.APH_v_tube(Do, td, Nc, Nr, m_gas, rho_gas)
    Di = Calculations_APH_tube.APH_Di(Do, td)
    #L_tot = Calculations_APH_boxsize.APH_L_tot(L, Ncross)

    DeltaP_tube = rho_gas * f_tube * L * np.power(v_tube, 2)/(2*Di) + rho_gas * K * np.power(v_tube, 2)/2
    return DeltaP_tube
    
#endregion
