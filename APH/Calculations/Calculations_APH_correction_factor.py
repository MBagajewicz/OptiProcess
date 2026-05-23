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
from APH.Calculations import Calculations_APH_effectiveness,Calculations_APH_NTU
from Common_Equations_HEX import Calculations_HEX_LMTD
#endregion


#region Calculations
def APH_F(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out, Tair_out):
    # LMTD correction factor
    Eff = Calculations_APH_effectiveness.APH_Eff(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out)
    NTU = Calculations_APH_NTU.APH_NTU(Cp_air, m_air, Cp_gas, m_gas, Tgas_in, Tair_in, Tgas_out)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(Tgas_in, Tgas_out, Tair_in, Tair_out)

    F = Eff * (Tgas_in - Tair_in) / ( NTU * LMTD )
    return F

#endregion
