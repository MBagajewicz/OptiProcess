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
from Aircooler.Calculations import Calculations_aircooler_Aot
#endregion

#region Calculations

def aircooler_area(Dte, Lf, tf, Nf, Nbay, Nbbay, Nr, Ntr, L):
    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    A = Nbay*Nbbay*Nr*Ntr*Aot*L
    return A

#endregion