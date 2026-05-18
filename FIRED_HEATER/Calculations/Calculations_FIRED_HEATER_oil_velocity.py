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

def HEATER_Foil_Tube(Moil, Npasses):
    # flow of oil in each ntshield tube 
    Foil_Tube = Moil/Npasses
    return Foil_Tube

def HEATER_Voil_Tube(Do, Moil, Npasses, rho_oil ):
    # velocity of oil in each tube
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)
    Foil_Tube = HEATER_Foil_Tube(Moil, Npasses)
    Voil_Tube = Foil_Tube/(rho_oil * 3.1416 * np.power(Di_Tube,2)/4)
    return Voil_Tube

