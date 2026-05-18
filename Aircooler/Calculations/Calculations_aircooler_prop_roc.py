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

def aircooler_calc_prop_air_roc(Tco, Tci):
# Air physical properties are considered constant using a temperature reference equivalent to the mean
# temperature between inlet and outlet
    # Temperature reference
    Tcm = (Tco+Tci)/2 #+ 273.15
    # Density (kg/m³)
    roc = 1.4107e-11*Tcm**4 - 2.1124e-8*Tcm**3 + 1.2845e-5*Tcm**2 - 4.5851e-3*Tcm + 1.2942
    return roc

#endregion

