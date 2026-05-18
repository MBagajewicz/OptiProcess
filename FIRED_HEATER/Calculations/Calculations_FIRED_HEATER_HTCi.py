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

def HEATER_HTCi(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil):
    # heat transfer coefficient inside the tubes
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)
    HTCi = (Pr_oil**0.33)* 0.023 *( k_oil/np.power(Di_Tube,1.8) )*np.power(4*Moil/(Npasses*3.141516*mu_oil), 0.8)
    return HTCi

