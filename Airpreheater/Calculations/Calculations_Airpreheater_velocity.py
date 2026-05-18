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

def Airpreheater_velocity(Ntp, Lw, Np, bp, ms, ros):
    # Velocity
    Nc = Ntp - 1
    Ac = bp*Lw
    msc = 2*ms*Np/(Nc)
    vc = msc/ros/Ac
    return vc

#endregion