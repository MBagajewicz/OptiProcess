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
from APH.Calculations import Calculations_APH_capacity_rate_ratio, Calculations_APH_effectiveness
import numpy as np
#endregion


#region Calculations

def APH_NTU(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out):
    # number of transfer units
    Cr = Calculations_APH_capacity_rate_ratio.APH_Cr(Cp_air, m_air, Cp_gas, m_gas)
    Eff = Calculations_APH_effectiveness.APH_Eff(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out)

    NTU = -np.log(1+np.power(Cr,1.15)*np.log(1-Eff))/np.power(Cr,1.15)
    return NTU  

#endregion
