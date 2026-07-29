#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
##################################################################################################################
#endregion

#region Calculations
def SPHE_velocity(mh, mc, H, dh, dc, roh, roc):
    # Shell-side velocity
    
    Ah = H  * dh 
    vh = (mh ) / (roh  * Ah)

    Ac = H  * dc 
    vc = (mc ) / (roc  * Ac)
    
    return vh, vc


def SPHE_velocity_lb(mh, mc, H, dh, dc, romax, romin):
    # Shell-side velocity

    Ah = H * dh 
    vhlb = (mh ) / (romax  * Ah)

    Ac = H  * dc 
    vclb = (mc ) / (romax  * Ac)

    return vhlb, vclb

def SPHE_velocity_ub(mh, mc, H, dh, dc, romax, romin):
    # Shell-side velocity

    Ah = H  * dh 
    vhub = (mh ) / (romin  * Ah)

    Ac = H  * dc 
    vcub = (mc ) / (romin  * Ac)

    return vhub, vcub
#endregion