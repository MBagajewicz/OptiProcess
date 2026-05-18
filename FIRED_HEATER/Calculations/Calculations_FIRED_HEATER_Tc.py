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
import math
import numpy as np
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Q_radiant
#endregion


#region Calculations

def HEATER_Tc_LB(Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad):
    # Lower Bound Tc for oil
    Oil_Entho = Enthoil_c1*np.power(To_oil,2) + Enthoil_c2*To_oil + Enthoil_c3
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)

    expr = 4* Enthoil_c1 * Moil *(-Enthoil_c3* Moil + Oil_Entho * Moil + Qrad_UB*(percent_loss_Rad-1))+np.power(Enthoil_c2,2)*np.power(Moil,2)
    Tc_LB = np.where(expr > 0, (np.sqrt(expr) - Enthoil_c2 * Moil) / (2 * Enthoil_c1 * Moil), np.nan)
    return Tc_LB


def HEATER_Tc_UB(Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad):
    # Upper bound Tc for oil
    Oil_Entho = Enthoil_c1*np.power(To_oil,2) + Enthoil_c2*To_oil + Enthoil_c3
    Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad)
    Tc_UB = ( np.sqrt( 4* Enthoil_c1 * Moil *(-Enthoil_c3* Moil + Oil_Entho * Moil + Qrad_LB*(percent_loss_Rad-1)) + np.power(Enthoil_c2,2)*np.power(Moil,2)) - Enthoil_c2*Moil ) / (2*Enthoil_c1*Moil)
    return Tc_UB