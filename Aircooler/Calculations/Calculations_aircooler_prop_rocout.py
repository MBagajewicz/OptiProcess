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

def aircooler_calc_rocout(Tco):
    # Density (kg/m³)
    rocout = 1.41107e-11*Tco**4 - 2.1124e-8*Tco**3 + 1.2845e-5*Tco**2 - 4.5851e-3*Tco + 1.2942
    return rocout

#endregion

