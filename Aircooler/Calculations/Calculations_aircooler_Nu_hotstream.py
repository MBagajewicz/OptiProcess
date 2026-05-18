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
#endregion

#region Calculations

def aircooler_Nusselt_hotstream(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kh):
    # Nusselt number of hot stream
    Reh = Calculations_aircooler_Re_hotstream.aircooler_Reynolds_hotstream(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih)
    Prh = (Cph*mih) / kh
    Nuh = 0.023*(Reh**0.8)*(Prh**(1/3))
    return Nuh

#endregion
