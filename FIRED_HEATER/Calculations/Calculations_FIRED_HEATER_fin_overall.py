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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Aot, Calculations_FIRED_HEATER_fin_efficiency
#endregion


#region Calculations

def HEATER_nut_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # overall efficienct of the finned surface depends on the fin efficiency
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(lf, Do, tf, Nf)
    Aof = Calculations_FIRED_HEATER_Aot.HEATER_Aof(lf, Do, tf, Nf)
    nuf_LB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_nuf_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)

    nut_LB = (Aot-Aof)/Aot + nuf_LB*(Aof/Aot)
    return nut_LB


def HEATER_nut_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin):
    # overall efficienct of the finned surface depends on the fin efficiency
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(lf, Do, tf, Nf)
    Aof = Calculations_FIRED_HEATER_Aot.HEATER_Aof(lf, Do, tf, Nf)
    nuf_UB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_nuf_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Nrconv, Rpv, Flux_Min, Tfb_Min, Pr_gas, rf_gas, k_fin)

    nut_UB = (Aot-Aof)/Aot + nuf_UB*(Aof/Aot)
    return nut_UB
