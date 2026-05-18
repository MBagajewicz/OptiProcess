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
from Aircooler.Calculations import Calculations_aircooler_Re_hotstream
from math import pi
#endregion


#region Calculations

def aircooler_deltaP_tube(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, L, roh):
    Reh = Calculations_aircooler_Re_hotstream.aircooler_Reynolds_hotstream(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih)
    Dti = Dte - 2*thk
    s = roh/1000
    # fh - friction factor
    fh = 0.4137*(Reh**(-0.2585))
    # Gh - mass flux of hot stream
    #Gh = (mh * (Npt / (Ntr*Nr*Nbay*Nbbay))) / (pi * (Dti**2) / 4)
    Gh = 4*mh*(Npt/Ntr/Nr/Nbay/Nbbay)/pi/(Dti**2)
    # DeltaP_f - The pressure drop caused by the fluid flow inside the tubes
    #dPf = (fh * Npt * (Gh**2) * L) / (2*roh*(Dti**2))
    dPf = fh * Npt * (Gh**2) * L / 2000 / Dti / s
    # alphar - depends on the number of tube passes
    alphar = 2*Npt - 1.5
    # DeltaP_r - The heads pressure drop
    #dPr = ((Gh**2) * alphar) / (2*roh)
    dPr = (5e-4 / s) * alphar * (Gh**2)
    # DeltaP_h - tube-side pressure drop
    dPh = dPf + dPr
    return dPh

#endregion

