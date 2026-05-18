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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Q_conv, Calculations_FIRED_HEATER_Tfb, Calculations_FIRED_HEATER_cp_gas, Calculations_FIRED_HEATER_gas_flow

#endregion


#region Calculations

def HEATER_Hfb_LB(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame):
    # gas enthalpy
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    Hfb_LB = hflame + cp_gas*(Tfb_LB - Tflame)
    return Hfb_LB

def HEATER_Hfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame):
    # gas enthalpy
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max)
    Hfb_UB = hflame + cp_gas*(Tfb_UB - Tflame)
    return Hfb_UB

def HEATER_Hstack_LB(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3):
    # stack enthalpy
    Hfb_LB = HEATER_Hfb_LB(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame)
    Qconv_UB2 = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_UB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, percent_loss_Conv)
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    Hstack_LB = Hfb_LB - (1-percent_loss_Conv) *  Qconv_UB2/Mgas_LB
    return Hstack_LB

def HEATER_Hstack_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3):
    # stack enthalpy
    Hfb_UB = HEATER_Hfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame)
    Qconv_LB2 = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_LB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, percent_loss_Conv)
    Mgas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max)
    Hstack_UB = Hfb_UB - (1-percent_loss_Conv) *  Qconv_LB2/Mgas_UB
    return Hstack_UB

