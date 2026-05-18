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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Q_radiant, Calculations_FIRED_HEATER_area_flow, Calculations_FIRED_HEATER_cp_gas
#endregion


#region Calculations

def HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min):
    # Lower bound on gas flow rate
    Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Mgas_LB = Qrad_LB*(1 - percent_loss_Rad)/(cp_gas*(Tflame - Tfb_Min))
    return Mgas_LB

def HEATER_Mgas_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max):
    # upper bound on gas flow rate
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Mgas_UB = Qrad_UB*(1 - percent_loss_Rad)/(cp_gas*(Tflame - Tfb_Max))
    return Mgas_UB

def HEATER_Ggas_LB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf):
    # lower bound on gas mass flux
    Mgas_LB = HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    As = Calculations_FIRED_HEATER_area_flow.HEATER_As(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf)
    Ggas_LB = Mgas_LB / As
    return Ggas_LB

def HEATER_Ggas_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf):
    # upper bound on gas mass flux
    Mgas_UB = HEATER_Mgas_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max)
    As = Calculations_FIRED_HEATER_area_flow.HEATER_As(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf)
    Ggas_UB = Mgas_UB / As
    return Ggas_UB



def HEATER_Gstack_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Ds):
    # stack mass flux
    Mgas_LB = HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    Gstack_LB = Mgas_LB / (np.pi * np.power(Ds,2)/4)
    return Gstack_LB
