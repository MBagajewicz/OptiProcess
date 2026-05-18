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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_pressure_conv, Calculations_FIRED_HEATER_pressure_minor, Calculations_FIRED_HEATER_pressure_stack
#endregion


#region Calculations


def HEATER_Fsum_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv, Nrconv, Flux_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min, Hs, Ds):
    # friction lossses
    DPconv_LB = Calculations_FIRED_HEATER_pressure_conv.HEATER_DPconv_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv, Nrconv, Flux_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)

    DPstack_LB = Calculations_FIRED_HEATER_pressure_stack.HEATER_DPstack_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Flux_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max, Hs, Ds)

    DPminor_LB = Calculations_FIRED_HEATER_pressure_minor.HEATER_DPminor_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ds, Flux_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)

    Fsum_LB = DPconv_LB + DPstack_LB + DPminor_LB
    return Fsum_LB

