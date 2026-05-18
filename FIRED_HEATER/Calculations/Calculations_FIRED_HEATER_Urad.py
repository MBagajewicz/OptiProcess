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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_pressure, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_Nuoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil, Pr_oil):
    Reoil_Tube = Calculations_FIRED_HEATER_pressure.HEATER_Reoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil)

    Nuoil_Tube = 0.023 * np.power(Reoil_Tube,0.8) * np.power(Pr_oil,0.33)    
    return Nuoil_Tube

def HEATER_hctoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil, Pr_oil, k_oil):
    Nuoil_Tube = HEATER_Nuoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil, Pr_oil)
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)

    hctoil_Tube = Nuoil_Tube * k_oil/Di_Tube
    return hctoil_Tube

def HEATER_Urad(Do, Moil, Npasses, rho_oil, mu_oil, Pr_oil, k_oil, rf_gas, ks, rf_oil):
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)
    hctoil_Tube = HEATER_hctoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil, Pr_oil, k_oil)

    Urad = 1/(rf_gas + Do * np.log(Do/Di_Tube)/(2*ks) + rf_oil * (Do/Di_Tube)+(1/hctoil_Tube)*(Do/Di_Tube))
    return Urad
