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
from APH.Calculations import Calculations_APH_heat_load
#endregion


#region Calculations

def APH_Eff(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out):
    # heat exchanger effectiveness
    Qmax = Calculations_APH_heat_load.APH_Qmax(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in)
    Q = Calculations_APH_heat_load.APH_Q(Cp_gas, m_gas, Tgas_in, Tgas_out)

    Eff = Q/Qmax
    return Eff

#endregion
