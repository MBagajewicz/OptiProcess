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

def aircooler_Gh(Dte, thk, mh, Npt, Ntr, Nr, Nbay, Nbbay):
   Dti = Dte - 2*thk
   #Gh = (4*mh*(Npt/Ntr/Nr/Nbay/Nbbay))/pi/(Dti**2)
   Gh = (mh*(Npt/(Ntr*Nr*Nbay*Nbbay))/(pi*((Dti**2)/4)))
   return Gh

#endregion

