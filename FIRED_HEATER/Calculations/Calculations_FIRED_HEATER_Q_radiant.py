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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_area_radiant
#endregion


#region Calculations

def HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad):
    # Upper bound on Qrad
    ARad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pk1, Nprad, Npconv, Npasses, Do)
    Qrad_UB = ARad * Flux_Max / (1 - percent_loss_Rad)
    return Qrad_UB

def HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad):
    # Upper bound on Qrad
    ARad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pk1, Nprad, Npconv, Npasses, Do)
    Qrad_LB = ARad * Flux_Min / (1 - percent_loss_Rad)
    return Qrad_LB