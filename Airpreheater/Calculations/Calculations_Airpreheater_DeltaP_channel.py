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
from Airpreheater.Calculations import Calculations_Airpreheater_frictionfactor, Calculations_Airpreheater_Reynolds, Calculations_Airpreheater_velocity
#endregion

#region Calculations

def Airpreheater_DeltaP_channel(Ntp, Lp, Lw, Dp, Np, Sa, bp, phi, ros, mis, ms):
    # Channel pressure drop
    ft = Calculations_Airpreheater_frictionfactor.Airpreheater_frictionfactor(Ntp, Lw, Np, Sa, bp, phi, ros, mis, ms)
    Red = Calculations_Airpreheater_Reynolds.Airpreheater_Reynolds(Ntp, Lw, Np, bp, phi, ros, mis, ms)
    vs = Calculations_Airpreheater_velocity.Airpreheater_velocity(Ntp, Lw, Np, bp, ms, ros)
    Deq = 2*bp/phi
    DP_c = ft*Np*(Lp+Dp)*vs**2/Deq/2*ros/100000
    return DP_c

#endregion