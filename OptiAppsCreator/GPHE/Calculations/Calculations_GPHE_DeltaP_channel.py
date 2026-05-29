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
from GPHE.Calculations import Calculations_GPHE_frictionfactor, Calculations_GPHE_Reynolds, Calculations_GPHE_velocity
#endregion

#region Calculations

def GPHE_DeltaP_channel(Ntp, Lp, Lw, Dp, Np, Sa, bp, phi, ros, mis, ms):
    # Channel pressure drop
    ft = Calculations_GPHE_frictionfactor.GPHE_frictionfactor(Ntp, Lw, Np, Sa, bp, phi, ros, mis, ms)
    Red = Calculations_GPHE_Reynolds.GPHE_Reynolds(Ntp, Lw, Np, bp, phi, ros, mis, ms)
    vs = Calculations_GPHE_velocity.GPHE_velocity(Ntp, Lw, Np, bp, ms, ros)
    Deq = 2*bp/phi
    DP_c = ft*Np*(Lp+Dp)*vs**2/Deq/2*ros/100000
    return DP_c

#endregion