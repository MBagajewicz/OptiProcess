#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion


#region Import Library
from Kettle.Calculations import Calculations_Kettle_countingtable
from math import pi
#endregion

#region Calculations

def Kettle_area(Ds, dte, Npt, rp, lay, L):
    # Heat exchanger area
    Ntt = Calculations_Kettle_countingtable.Kettle_counting_table(Ds, dte, Npt, rp, lay)
    A = Ntt * pi * dte * L
    return A