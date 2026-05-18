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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Tc, Calculations_FIRED_HEATER_Tfb, Calculations_FIRED_HEATER_Ts
from Common_Equations_HEX import Calculations_HEX_LMTD
#endregion


#region Calculations

def HEATER_LMTD_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    # Upper bound for LMTD
    Ts_LB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max)
    Tc_LB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_LB(Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad)
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)

    #if Ts_LB - Ti_oil > 0 :
    #    LMTD_UB = Calculations_HEX_LMTD.HEX_lmtd(Tfb_UB, Ts_LB, Ti_oil, Tc_LB)
    #    return LMTD_UB
    #else :
    #    return np.maximum(Tfb_UB-Tc_LB, Ts_UB-Ti_oil)
    condition = (Ts_LB - Ti_oil) > 0
    #LMTD_UB_case1 = Calculations_HEX_LMTD.HEX_lmtd(Tfb_UB, Ts_LB, Ti_oil, Tc_LB)
    LMTD_UB_case1 = ((Tfb_UB - Tc_LB) - (Ts_LB - Ti_oil)) / np.log((Tfb_UB - Tc_LB)/(Ts_LB - Ti_oil))
    LMTD_UB_case2 = np.maximum(Tfb_UB - Tc_LB, Ts_UB - Ti_oil)
    
    LMTD_UB = np.where(condition, LMTD_UB_case1, LMTD_UB_case2)
    return LMTD_UB



def HEATER_LMTD_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, Tfb_Max, hflame, percent_loss_Conv, Ti_oil):
    # Lower bound for LMTD
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    Tc_UB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_UB(Enthoil_c1, Enthoil_c2, Enthoil_c3, To_oil, Moil, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad)
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max)

    #if Tfb_LB - Tc_UB > 0 :
    #    LMTD_LB = Calculations_HEX_LMTD.HEX_lmtd(Tfb_LB, Ts_UB, Ti_oil, Tc_UB)
    #    return LMTD_LB
    #else :
    #    return np.minimum(Tfb_UB - Tc_UB, Ts_UB - Ti_oil)
    condition = (Tfb_LB - Tc_UB) > 0
    #LMTD_LB_case1 = Calculations_HEX_LMTD.HEX_lmtd(Tfb_LB, Ts_UB, Ti_oil, Tc_UB)
    LMTD_LB_case1 = ((Tfb_LB - Tc_UB) - (Ts_UB - Ti_oil)) / np.log((Tfb_LB - Tc_UB)/(Ts_UB - Ti_oil))
    LMTD_LB_case2 = np.minimum(Tfb_UB - Tc_UB, Ts_UB - Ti_oil)

    LMTD_LB = np.where(condition, LMTD_LB_case1, LMTD_LB_case2)
    return LMTD_LB


