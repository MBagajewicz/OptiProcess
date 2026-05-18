#
# region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
# endregion

# region Calculations

def aircooler_calc_prop_air_kc(Tco, Tci):
    # Temperature reference
    Tcm = (Tco+Tci)/2 # + 273.15
    # Thermal Conductivity (W/m.K)
    kc = -2.7221e-8*Tcm**2 + 7.8051e-5*Tcm + 2.4134e-2
    return kc

# endregion