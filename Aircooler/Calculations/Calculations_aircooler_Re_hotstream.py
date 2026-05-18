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
#endregion

#region Calculations

def aircooler_Reynolds_hotstream(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih):
    # Reynolds number of hot stream
    Dti = Dte - 2*thk
    #Reh = (4*Npt*mh)/(pi*Dti*Nbay*Nbbay*Ntr*Nr*mih)
    Reh = 4*mh*Npt/pi/mih/Dti/Nbay/Nbbay/Ntr/Nr
    return Reh

#endregion
