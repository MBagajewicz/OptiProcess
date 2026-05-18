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

def HEATER_As(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf):
    # flow area in the centrak plane of a tube row
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Wconv = Calculations_FIRED_HEATER_boxsize.HEATER_Wconv(Npconv, Npasses, lf, Do, Rph)
    Ntshield = Calculations_FIRED_HEATER_tubes.HEATER_Ntshield(Npconv, Npasses)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    As = El *( Wconv - Ntshield *( Do + Nf * (df - Do) * tf ))
    return As
