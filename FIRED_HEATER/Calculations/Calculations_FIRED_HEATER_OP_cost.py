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
from math import pi
import numpy as np
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_cp_gas, Calculations_FIRED_HEATER_Q_conv, Calculations_FIRED_HEATER_Q_radiant, Calculations_FIRED_HEATER_Q_oil

#endregion

#region Calculations

def HEATER_Mfeul_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ti_oil, T_outside, Moil, Flux_Max, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, LHV):
    # Lower bound of operating cost
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Qs_LB = Mgas_LB * cp_gas * (Ti_oil - T_outside)
    Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad)
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Qn_LB = Qrad_LB + (Qoil - Qrad_UB) + Qs_LB

    Mfuel_LB = Qn_LB / LHV
    return Mfuel_LB


def HEATER_OP_cost_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ti_oil, T_outside, Moil, Flux_Max, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, LHV, O_uni, OT):
    Mfuel_LB = HEATER_Mfeul_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ti_oil, T_outside, Moil, Flux_Max, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, LHV)
    
    OP_cost_LB = Mfuel_LB * O_uni * OT
    return OP_cost_LB
