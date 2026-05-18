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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Q_oil, Calculations_FIRED_HEATER_Tfb, Calculations_FIRED_HEATER_cp_gas, Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_stack_enthalpy
#endregion


#region Calculations

def HEATER_Ts_UB1(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    # inlet stack temperature
    Hstack_UB = Calculations_FIRED_HEATER_stack_enthalpy.HEATER_Hstack_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Hfb_LB = Calculations_FIRED_HEATER_stack_enthalpy.HEATER_Hfb_LB(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max)
    Ts_UB1 = (Hstack_UB- Hfb_LB)/cp_gas + Tfb_UB
    return Ts_UB1

def HEATER_Ts_LB1(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    # inlet stack temperature
    Hstack_LB = Calculations_FIRED_HEATER_stack_enthalpy.HEATER_Hstack_LB(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Hfb_UB = Calculations_FIRED_HEATER_stack_enthalpy.HEATER_Hfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    Ts_LB1 = (Hstack_LB- Hfb_UB)/cp_gas + Tfb_LB
    return Ts_LB1

def HEATER_Ts_UB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max):
    # exit gas temperature of convection section
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Mgas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)    
    Ts_UB2 = Tflame - Qoil/ (Mgas_UB* cp_gas)
    #Ts_UB2 =  Tfb_UB - Qconv_LB2*(1-percent_loss_Conv)/ (Mgas_UB * cp_gas)
    return Ts_UB2

def HEATER_Ts_LB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min):
    # exit gas temperature of convection section
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)    
    Ts_LB2 = Tflame -  Qoil/ (Mgas_LB* cp_gas)
    #Ts_LB2 = Tfb_LB - Qconv_UB2*(1-percent_loss_Conv)/ (Mgas_LB* cp_gas)
    return Ts_LB2



def HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    # choose Ts_UB
    Ts_UB1 = HEATER_Ts_UB1(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Ts_UB2 = HEATER_Ts_UB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max)
    Ts_UB = np.minimum(Ts_UB1, Ts_UB2)
    return Ts_UB

def HEATER_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    # choose Ts_LB
    Ts_LB1 = HEATER_Ts_LB1(Tflame,L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)
    Ts_LB2 = HEATER_Ts_LB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    Ts_LB = np.maximum(Ts_LB1, Ts_LB2)
    return Ts_LB