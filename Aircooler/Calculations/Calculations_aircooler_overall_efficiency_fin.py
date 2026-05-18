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
from math import pi
import numpy as np
from Aircooler.Calculations import Calculations_aircooler_Ar, Calculations_aircooler_Aot, Calculations_aircooler_hc
#endregion

#region Calculations

def aircooler_overall_efficiency_fin(Lf, Dte, tf, Nf, rp, Ntr, Nbay, Nbbay, L, Tco, Tci, Rfc, kf, mh, Cph, Thi, Tho):
    # Overall efficiency of the finned surface
    # Df = fin diameter
    Df = Dte + 2*Lf
    Ar = Calculations_aircooler_Ar.aircooler_Ar(Dte)
    # Ab = area of the root tube
    Ab = Ar * (1 - tf * Nf)
    # Aof = fin area
    Aof = 2*Nf*(pi/4) * (Df**2 - Dte**2) + pi*Df*tf*Nf
    # Aot = the total finned surface area per unit length
    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    # etaf = efficiency of an individual fin
    hc = Calculations_aircooler_hc.aircooler_coefficient_hc(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho,
                                                            Tco, Tci)
    hl = hc/(1+Rfc*hc)
    mf = ((2*hl)/(kf*tf))**0.5
    Lfe = Lf*(1+(tf/2*Lf))*(1+0.35*np.log(Df/Dte))
    etaf = np.tanh(mf*Lfe)/(mf*Lfe)
    # Efficiency
    etat = ((Aot-Aof)/Aot) + etaf*(Aof/Aot)
    return etat

#endregion
