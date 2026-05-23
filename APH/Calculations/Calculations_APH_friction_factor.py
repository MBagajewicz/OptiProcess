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
from APH.Calculations import Calculations_APH_velocity, Calculations_APH_Reynolds
import numpy as np
#endregion


#region Calculations
def APH_f_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air):
    # friction factor_Kern method (air side)
    Re_air = Calculations_APH_Reynolds.APH_Re_air(Nr, Do, rpv, lf, rph, L, m_air, rho_air, mu_air)

    f_air = 1.728 * np.power(Re_air, -0.188)
    return f_air


def APH_f_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas):
    # Fanning friction factor (tube side)
    Re_tube = Calculations_APH_Reynolds.APH_Re_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas)

    # --- 배열 입력에도 대응하도록 np.where 사용 ---
    f_tube = np.zeros_like(Re_tube, dtype=float)

    # 식 정의
    cond1 = (Re_tube < 1311)
    cond2 = (Re_tube >= 1311) & (Re_tube < 3380)
    cond3 = (Re_tube >= 3380)

    f_tube = np.where(cond1, 16 / Re_tube,
               np.where(cond2, 0.048,
               0.014 + 1.056 / (Re_tube ** 0.42)))

    return f_tube



#    if Re_tube <= 1311.0:
#        f_tube = 16.0 / Re_tube
#        return f_tube
#    elif Re_tube < 3380.0:
#        f_tube = 0.048
#        return f_tube
#    else:
#        f_tube = 0.014 + 1.056 / np.power(Re_tube,0.42)
#        return f_tube

#endregion
