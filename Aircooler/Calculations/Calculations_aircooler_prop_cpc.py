#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Calculations

def aircooler_calc_prop_air_Cpc(Tco, Tci):
    # Temperature reference
    Tcm = (Tco+Tci)/2  #+ 273.15
    # Heat capacity (J/kg.K)
    Cpc = -3.6649e-7*Tcm**3 + 4.8370e-4*Tcm**2 + 1.77e-2*Tcm + 1008.9
    return Cpc

#endregion
