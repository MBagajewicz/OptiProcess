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

def APH_Pr_air(Cp_air, mu_air, k_air):
    # air side prandtl
    Pr_air = Cp_air * mu_air / k_air
    return Pr_air

def APH_Pr_tube(Cp_gas, mu_gas, k_gas):
    # tube side prandtl
    Pr_tube = Cp_gas * mu_gas / k_gas
    return Pr_tube


#endregion
