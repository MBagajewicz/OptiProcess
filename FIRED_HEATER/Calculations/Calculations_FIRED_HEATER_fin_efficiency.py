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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_HTCo, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_h1_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas):
    # parameter for fin efficiency
    HTCo_LB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas)
    h1_LB = 1 /( (1 / HTCo_LB) + rf_gas )
    return h1_LB

def HEATER_h1_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas, rf_gas):
    # parameter for fin efficiency
    HTCo_UB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas)
    h1_UB = 1 /( (1 / HTCo_UB) + rf_gas )
    return h1_UB    

def HEATER_Lfe(lf, tf, Do):
    # parameter for fin efficiency
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    Lfe = lf * (1 + tf/(2*lf)) * (1+ 0.35*np.log(df/Do))
    return Lfe

def HEATER_mf_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # parameter for fin efficiency
    h1_LB = HEATER_h1_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas)
    mf_LB = np.sqrt(2*h1_LB/(k_fin*tf))
    return mf_LB

def HEATER_mf_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas, rf_gas, k_fin):
    # parameter for fin efficiency
    h1_UB = HEATER_h1_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas, rf_gas)
    mf_UB = np.sqrt(2*h1_UB/(k_fin*tf))
    return mf_UB

def HEATER_nuf_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # fin efficiency
    mf_LB = HEATER_mf_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    Lfe = HEATER_Lfe(lf, tf, Do)
    mf_UB = HEATER_mf_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas, rf_gas, k_fin)
    nuf_LB = np.tanh(mf_LB * Lfe)/(mf_UB * Lfe)
    return nuf_LB

def HEATER_nuf_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # fin efficiency
    mf_LB = HEATER_mf_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)
    Lfe = HEATER_Lfe(lf, tf, Do)
    mf_UB = HEATER_mf_UB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Max, Tfb_Max, Pr_gas, rf_gas, k_fin)
    nuf_UB = np.tanh(mf_UB * Lfe)/(mf_LB * Lfe)
    return nuf_UB



