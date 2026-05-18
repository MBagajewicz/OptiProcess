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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_Ab(Do, tf, Nf):
    # exposed area of the root tube
    Ab = 3.141516 * Do * (1 - tf * Nf)
    return Ab

def HEATER_Aof(lf, Do, tf, Nf):
    # area of the fins
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    Aof = ((3.141516/2) * (np.power(df,2)-np.power(Do,2)) + 3.141516*df*tf ) * Nf
    return Aof

def HEATER_Aot(lf, Do, tf, Nf):
    Ab = HEATER_Ab(Do, tf, Nf)
    Aof = HEATER_Aof(lf, Do, tf, Nf)
    Aot = Ab + Aof
    return Aot


