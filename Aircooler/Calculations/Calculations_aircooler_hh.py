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
from Aircooler.Calculations import Calculations_aircooler_Nu_hotstream
#endregion

#region Calculations

def aircooler_coefficient_hh(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih, Cph, kh):
   # Heat-transfer coefficient of hot stream
   Dti = Dte - 2*thk
   Nuh = Calculations_aircooler_Nu_hotstream.aircooler_Nusselt_hotstream(Dte, thk, Npt, mh, Nbay, Nbbay, Ntr, Nr, mih,
                                                                         Cph, kh)
   hh = (Nuh*kh)/Dti
   return hh

#endregion