#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from Airpreheater.Calculations import Calculations_Airpreheater_velocity
#endregion

#region Calculations

def Airpreheater_Reynolds(Ntp, Lw, Np, bp, phi, ros, mis, ms):
    # Reynolds
    Nc = Ntp - 1
    Deq = 2*bp/phi
    vs = Calculations_Airpreheater_velocity.Airpreheater_velocity(Ntp, Lw, Np, bp, ms, ros)
    Red = Deq*vs*ros/mis
    return Red

#endregion
