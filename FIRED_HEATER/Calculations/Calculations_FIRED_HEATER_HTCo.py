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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_cp_gas, Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_j_factor
#endregion


#region Calculations

def HEATER_HTCo_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas):
    # convective heat transfer coefficient for the flue gas flow around the finned surface
    j_factor_LB = Calculations_FIRED_HEATER_j_factor.HEATER_j_factor_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Ggas_LB =Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_LB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf)
    HTCo_LB = j_factor_LB * cp_gas * Ggas_LB * np.power(Pr_gas, -0.67)
    return HTCo_LB

def HEATER_HTCo_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas):
    # convective heat transfer coefficient for the flue gas flow around the finned surface
    j_factor_UB = Calculations_FIRED_HEATER_j_factor.HEATER_j_factor_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv)
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(Tflame)
    Ggas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf)
    HTCo_UB = j_factor_UB * cp_gas * Ggas_UB * np.power(Pr_gas, -0.67)
    return HTCo_UB

