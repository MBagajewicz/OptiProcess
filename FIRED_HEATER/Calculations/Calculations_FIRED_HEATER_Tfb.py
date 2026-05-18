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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Q_radiant, Calculations_FIRED_HEATER_cp_gas, Calculations_FIRED_HEATER_gas_flow
#endregion


#region Calculations

def HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min):
    # Lower Bound of Tfb
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_LB = Tflame - Qrad_UB*(1-percent_loss_Rad) /(Mgas_LB*cp_gas)
    return Tfb_LB

def HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max):
    # Upper Bound of Tfb
    Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad)
    Mgas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Tfb_UB = Tflame - Qrad_LB*(1-percent_loss_Rad) /(Mgas_UB*cp_gas)
    return Tfb_UB

