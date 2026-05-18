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
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
from Aircooler.Calculations import Calculations_aircooler_U
#endregion
######################################################################################################################

#region Calculations

def aircooler_areq(Thi, Tho, Tci, Tco, Npt, Dte, thk, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kt, kh, Lf, tf, Nf, rp, L,
                   Rfc, Rfh, kf, F):
    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    U = Calculations_aircooler_U.aircooler_U(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kt, kh, Lf, tf, Nf, rp,
                                             L, Tco, Tci, Rfc, Rfh, kf, Thi, Tho)
    deltatlm = Calculations_HEX_LMTD.HEX_lmtd(Thi, Tho, Tci, Tco)
    areq = Q / (U*deltatlm*F)
    return areq

#endregion