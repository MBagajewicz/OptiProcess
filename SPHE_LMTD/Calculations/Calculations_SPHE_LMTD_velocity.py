#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-07-2025     Javier Francesconi         Original
#   
##################################################################################################################
#endregion

#region Calculations
def SPHE_velocity(m, H, d, ro):
    # Channel velocity
    
    A = H  * d 
    v = (m ) / (ro  * A)
   
    return v


def SPHE_velocity_lb(m, H, d, romax):
    # Lower bound Channel velocity

    A = H * d
    vlb = (m ) / (romax  * A)

    return vlb

def SPHE_velocity_ub(m, H, d, romin):
    # Upper bound Channel velocity

    A = H  * d 
    vub = (m ) / (romin  * A)
   

    return vub
#endregion