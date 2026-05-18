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
from Aircooler.Calculations import (
    Calculations_aircooler_hh,
    Calculations_aircooler_hc,
    Calculations_aircooler_Ar,
    Calculations_aircooler_Aot,
    Calculations_aircooler_overall_efficiency_fin
)
from math import pi
import numpy as np
#endregion


#region Calculations

def aircooler_U(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kt, kh, Lf, tf, Nf, rp, L, Tco, Tci, Rfc, Rfh, kf, Thi, Tho):
    hh = Calculations_aircooler_hh.aircooler_coefficient_hh(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kh)
    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    Dti = Dte - 2*thk
    hc = Calculations_aircooler_hc.aircooler_coefficient_hc(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho,
                                                            Tco, Tci)
    etat = Calculations_aircooler_overall_efficiency_fin.aircooler_overall_efficiency_fin(Lf, Dte, tf, Nf, rp, Ntr,Nbay,
                                                                                          Nbbay, L, Tco, Tci, Rfc, kf,
                                                                                          mh, Cph, Thi, Tho)
    U = 1 / ((1/hh + Rfh) * (Aot/pi/Dti) + (Aot*np.log(Dte/Dti))/2/pi/kt + 1/etat/hc + Rfc/etat)
    return U
