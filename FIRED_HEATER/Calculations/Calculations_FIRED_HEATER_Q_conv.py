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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Aconv, Calculations_FIRED_HEATER_LMTD, Calculations_FIRED_HEATER_Q_oil, Calculations_FIRED_HEATER_Q_radiant, Calculations_FIRED_HEATER_Uconv
#endregion


#region Calculations

def HEATER_Qconv_LB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, percent_loss_Conv):
    # Lower bound of Qconv (Btu/s)
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)
    Qconv_LB2 = (Qoil - Qrad_UB*(1-percent_loss_Rad))/(1-percent_loss_Conv)
    return Qconv_LB2

def HEATER_Qconv_UB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, percent_loss_Conv):
    # Upper bound of Qconv
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad) 
    Qconv_UB2 = (Qoil - Qrad_LB*(1-percent_loss_Rad))/(1-percent_loss_Conv)
    return Qconv_UB2

def HEATER_Qconv_LB1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad,Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv,Rph,mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, hflame, percent_loss_Conv, Ti_oil):
    Uconv_LB = Calculations_FIRED_HEATER_Uconv.HEATER_Uconv_LB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad,Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv,Rph,mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    Aconv = Calculations_FIRED_HEATER_Aconv.HEATER_Aconv(Npconv, Npasses, Nrconv, lf, Do, tf, Nf, L, pk1)
    LMTD_LB = Calculations_FIRED_HEATER_LMTD.HEATER_LMTD_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, Tfb_Max, hflame, percent_loss_Conv, Ti_oil)

    Qconv_LB1 = Uconv_LB* Aconv * LMTD_LB/(1-percent_loss_Conv)
    return Qconv_LB1

def HEATER_Qconv_UB1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Rph, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, hflame, percent_loss_Conv, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3):
    Uconv_UB = Calculations_FIRED_HEATER_Uconv.HEATER_Uconv_UB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Rph, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    Aconv = Calculations_FIRED_HEATER_Aconv.HEATER_Aconv(Npconv, Npasses, Nrconv, lf, Do, tf, Nf, L, pk1)
    LMTD_UB = Calculations_FIRED_HEATER_LMTD.HEATER_LMTD_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)

    Qconv_UB1 = Uconv_UB * Aconv *  LMTD_UB/(1-percent_loss_Conv)
    return Qconv_UB1

def HEATER_Qconv_UB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Rph, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, hflame, percent_loss_Conv, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3):
    Qconv_UB1 = HEATER_Qconv_UB1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Rph, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, hflame, percent_loss_Conv, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3)
    Qconv_UB2 = HEATER_Qconv_UB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, percent_loss_Conv)

    Qconv_UB = np.minimum(Qconv_UB1, Qconv_UB2)
    return Qconv_UB

def HEATER_Qconv_LB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad,Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv,Rph,mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, hflame, percent_loss_Conv, Ti_oil):
    Qconv_LB1 = HEATER_Qconv_LB1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad,Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv,Rph,mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, hflame, percent_loss_Conv, Ti_oil)
    Qconv_LB2 = HEATER_Qconv_LB2(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, percent_loss_Conv)

    Qconv_LB = np.maximum(Qconv_LB1, Qconv_LB2)
    return Qconv_LB
