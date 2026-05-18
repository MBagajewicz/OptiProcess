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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Aot, Calculations_FIRED_HEATER_boxsize, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_Aconv(Npconv, Npasses, Nrconv, lf, Do, tf, Nf, L, pk1):
    # convective heat transfer area
    Ntconv = Calculations_FIRED_HEATER_tubes.HEATER_Ntconv(Npconv, Npasses, Nrconv)
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(lf, Do, tf, Nf)
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)

    Aconv = Ntconv * Aot * El
    return Aconv


