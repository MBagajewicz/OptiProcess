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
from APH.Calculations import Calculations_APH_capacity_rate_ratio
#endregion


#region Calculations

def APH_Qmax(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in):
    # maximum heat load
    C_min = Calculations_APH_capacity_rate_ratio.APH_C_min(Cp_air, m_air, Cp_gas, m_gas)
    Qmax = C_min * (Tgas_in - Tair_in)
    return Qmax

def APH_Q(Cp_gas, m_gas, Tgas_in, Tgas_out):
    # heat load
    Q = Cp_gas * m_gas * (Tgas_in - Tgas_out)
    return Q



#endregion
