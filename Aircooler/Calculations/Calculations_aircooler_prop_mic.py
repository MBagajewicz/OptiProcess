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

def aircooler_calc_prop_air_mic(Tco, Tci):
    # Temperature reference
    Tcm = (Tco+Tci)/2  #+ 273.15
    # Viscosity (Pa.s)
    mic = 3.7778e-8*Tcm + 1.7487e-5
    return mic

#endregion