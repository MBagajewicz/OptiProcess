#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Sep-2025     Sung Young Kim            original
##################################################################################################################
#endregion

#region Import Library
from APH.Calculations import Calculations_APH_tube
from math import pi
#endregion


#region Calculations

def APH_Height(Nr, Do, rpv, lf):
    # height of air preheater
    delta_H = 1/12
    dcv = Calculations_APH_tube.APH_dcv(Do, rpv)
    Df = Calculations_APH_tube.APH_Df(Do, lf)

    H = (Nr-1)*dcv + Do/2 + Df + 2*delta_H
    return H

def APH_Width(Nc, Do, rph, lf):
    # width of air preheater
    delta_W = 1/12
    dch = Calculations_APH_tube.APH_dch(Do, rph)
    Df = Calculations_APH_tube.APH_Df(Do, lf)

    W = (Nc-1)*dch + dch/2 + Df + 2*delta_W
    return W

def APH_El(L, pk1):
    # exposed length
    El = L - pk1
    return El

def APH_lcs(L, Ncross):
    # cross flow stage length
    lcs = L/Ncross
    return lcs

def APH_FAR(rph):
    # flow area ratio (Kern's open-area fraction)
    FAR = 1 - 1/rph
    return FAR

def APH_L_eff(Nr, rpv, Do):
    # Total effective length with number of cross flows
    #L_eff = Ncross * ( (Nr-1)*rpv + Do )
    L_eff = ( (Nr-1)*rpv + Do )
    return L_eff

def APH_L_tot(L, Ncross):
    # Total tube flow length
    L_tot = Ncross * L
    return L_tot

#endregion
