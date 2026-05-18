#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Import Library
from Common_Equations_HEX import Calculations_HEX_LMTD
from Aircooler.Calculations import Calculations_aircooler_NUT
#endregion


#region Calculations

def f_base(Thi, Tho, Tci, Tco, mh, Cph):
    epsilon = (Thi - Tho) / (Thi - Tci)
    deltatlm = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
    NUT = Calculations_aircooler_NUT.aircooler_NUT(Thi, Tho, Tci, mh, Cph, Tco)
    fbase = (epsilon*(Thi - Tci)) / (deltatlm * NUT)
    return fbase

#endregion