#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Calculations

def GPHE_area(phi, Ntp, Lp, Lw):
    # Heat exchanger area
    A = phi*Ntp*Lp*Lw
    return A

#endregion
