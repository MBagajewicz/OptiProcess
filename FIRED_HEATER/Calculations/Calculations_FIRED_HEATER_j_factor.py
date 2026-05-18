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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_clearance, Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_tubes

#endregion


#region Calculations

def HEATER_C1_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas):
    # C1_LB for j factor
    Ggas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf)
    C1_LB = 0.091 * np.power( Do * Ggas_UB /mu_gas, -0.25)
    return C1_LB

def HEATER_C1_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas):
    # C1_UB for j factor
    Ggas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_LB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf)
    C1_UB = 0.091 * np.power( Do * Ggas_LB /mu_gas, -0.25)
    return C1_UB

def HEATER_C3(lf, Do, Nf, tf):
    # C3 for j factor
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    S = Calculations_FIRED_HEATER_clearance.HEATER_S(Nf, tf)
    C3 = 0.35 + 0.65 * np.exp(-0.125*( df - Do ) / S )
    return C3

def HEATER_C5(Nrconv, Do, Rpv, Rph):
    # C5 for j factor
    dcv = Calculations_FIRED_HEATER_tubes.HEATER_dcv(Do, Rpv)
    dch = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)
    C5 = 0.7 + ( 0.7 - 0.8 * np.exp(-0.15*np.power(Nrconv,2)) )*np.exp(-dcv/dch)
    return C5

def HEATER_j_factor_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv):
    # j factor for the convective heat transfer coefficient
    C1_LB = HEATER_C1_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas)
    C3 = HEATER_C3(lf, Do, Nf, tf)
    C5 = HEATER_C5(Nrconv, Do, Rpv, Rph)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    j_factor_LB = C1_LB * C3 * C5 * np.power(df/Do, 0.5)
    return j_factor_LB

def HEATER_j_factor_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv):
    # j factor for the convective heat transfer coefficient
    C1_UB = HEATER_C1_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas)
    C3 = HEATER_C3(lf, Do, Nf, tf)
    C5 = HEATER_C5(Nrconv, Do, Rpv, Rph)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    j_factor_UB = C1_UB * C3 * C5 * np.power(df/Do, 0.5)
    return j_factor_UB

