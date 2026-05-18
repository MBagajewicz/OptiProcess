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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Aot, Calculations_FIRED_HEATER_HTCi, Calculations_FIRED_HEATER_HTCo, Calculations_FIRED_HEATER_fin_overall, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_Uc1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil):
    HTCi = Calculations_FIRED_HEATER_HTCi.HEATER_HTCi(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil)
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(lf, Do, tf, Nf)
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)

    Uc1 = (1/HTCi + rf_oil)*(Aot/(3.141516*Di_Tube))
    return Uc1

def HEATER_Uc2(lf, Do, tf, Nf, ks):
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(lf, Do, tf, Nf)
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)

    Uc2 = Aot*np.log(Do/Di_Tube) / (2*3.141516*ks)
    return Uc2

def HEATER_Uc3_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    nut_UB = Calculations_FIRED_HEATER_fin_overall.HEATER_nut_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    HTCo_UB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas)
    
    Uc3_LB = 1/(nut_UB * HTCo_UB) + rf_gas/nut_UB
    return Uc3_LB

def HEATER_Uc3_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    nut_LB = Calculations_FIRED_HEATER_fin_overall.HEATER_nut_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    HTCo_LB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas)
    
    Uc3_UB = 1/(nut_LB * HTCo_LB) + rf_gas/nut_LB
    return Uc3_UB

def HEATER_Uconv_LB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad,Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv,Rph,mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # overall heat transfer coefficient for convection section
    Uc1 = HEATER_Uc1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil)
    Uc2 = HEATER_Uc2(lf, Do, tf, Nf, ks)
    Uc3_UB = HEATER_Uc3_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
        
    Uconv_LB = 1/(Uc1 + Uc2 + Uc3_UB)
    return Uconv_LB

def HEATER_Uconv_UB(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil, ks, L, pk1, Nprad, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Rph, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    Uc1 = HEATER_Uc1(Pr_oil, k_oil, Do, Moil, Npasses, mu_oil, lf, tf, Nf, rf_oil)
    Uc2 = HEATER_Uc2(lf, Do, tf, Nf, ks)
    Uc3_LB = HEATER_Uc3_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)

    Uconv_UB = 1/(Uc1 + Uc2 + Uc3_LB)
    return Uconv_UB
