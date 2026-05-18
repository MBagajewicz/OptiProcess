#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          22-Aug-2025     Sung Young Kim            Copy from GPHE folder

##################################################################################################################
#endregion

#region Calculations

def Airpreheater_area(phi, Ntp, Lp, Lw):
    # Heat exchanger area
    A = phi*Ntp*Lp*Lw
    return A

#endregion
