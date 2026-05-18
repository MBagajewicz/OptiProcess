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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_gas_density, Calculations_FIRED_HEATER_gas_flow
#endregion


#region Calculations



def HEATER_DPstack_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Flux_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max, Hs, Ds):
    # pressure drop along the stack
    Gstack_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Gstack_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ds)
    Tmean_stack = Calculations_FIRED_HEATER_gas_density.HEATER_Tmean_stack(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)

    DPstack_LB = 2.76e-5 * np.power(Gstack_LB,2) * (Tmean_stack/1.8) * Hs/Ds
    return DPstack_LB

