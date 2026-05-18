#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion

#region Calculations
def Kettle_shellside_velocity(ms, ros, Ds, rp, L, Nb):
    # Shell-side velocity
    qs = ms / ros
    FAR = 1 - 1 / rp
    lbc = (L / (Nb + 1))
    Ar = Ds * FAR * lbc
    vs = qs / Ar
    return vs

#endregion