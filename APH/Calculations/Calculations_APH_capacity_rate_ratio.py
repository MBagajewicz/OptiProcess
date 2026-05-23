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
#endregion


#region Calculations
def APH_C_min(Cp_air, m_air, Cp_gas, m_gas):
    C_air = Cp_air * m_air
    C_gas = Cp_gas * m_gas
    C_min = min(C_air, C_gas)
    return C_min    

def APH_C_max(Cp_air, m_air, Cp_gas, m_gas):
    C_air = Cp_air * m_air
    C_gas = Cp_gas * m_gas
    C_max = max(C_air, C_gas)
    return C_max    

def APH_Cr(Cp_air, m_air, Cp_gas, m_gas):
    # capacity rate ratio
    C_min = APH_C_min(Cp_air, m_air, Cp_gas, m_gas)
    C_max = APH_C_max(Cp_air, m_air, Cp_gas, m_gas)
    
    Cr = C_min/C_max
    return Cr

#endregion
