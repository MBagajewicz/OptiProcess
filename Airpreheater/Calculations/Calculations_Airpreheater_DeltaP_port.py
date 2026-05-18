#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from math import pi
#endregion

#region Calculations

def Airpreheater_DeltaP_port(Dp, Np, ms, ros):
    # Port pressure drop
    Ac = pi*Dp**2/4
    vs = ms/ros/Ac
    DP_p = 1.4*Np*vs**2*ros/2/100000
    return DP_p

#endregion