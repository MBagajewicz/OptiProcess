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

def aircooler_Ar(Dte):
    # Ar = outside bare area per unit length
    Ar = pi*Dte
    return Ar

#endregion