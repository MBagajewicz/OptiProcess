#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          24-Mar-2025     Sung Young Kim            Original

##################################################################################################################
#endregion

#region Import Library
import numpy as np
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_boxsize, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_ARad(L, pk1, Nprad, Npconv, Npasses, Do):
    # area of radiant section
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Ntrad = Calculations_FIRED_HEATER_tubes.HEATER_Ntrad(Nprad, Npconv, Npasses)
    ARad = Ntrad* El* 3.1416 * Do
    return ARad

