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
from Aircooler.Calculations import Calculations_aircooler_Ar
#endregion


#region Calculations

def aircooler_Aot(Dte, Lf, tf, Nf):
    # Df = fin diameter
    Df = Dte + 2*Lf
    Ar = Calculations_aircooler_Ar.aircooler_Ar(Dte)
    # Ab = area of the root tube
    Ab = Ar * (1 - tf * Nf)
    # Aof = fin area
    Aof = 2*Nf*(pi/4)*(Df**2 - Dte**2) + pi*Df*tf*Nf
    # Aot = the total finned surface area per unit length
    Aot = Ab + Aof
    return Aot

#endregion