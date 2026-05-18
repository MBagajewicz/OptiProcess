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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_Tfb, Calculations_FIRED_HEATER_Ts
#endregion


#region Calculations

# density of the gas at the convection section outlet
def HEATER_rho_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min):
    # Upper gas density 
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    rho_Tfb_UB = 2116.22045*27.777276 / (778.169 * 1.985 * Tfb_LB)
    return rho_Tfb_UB


def HEATER_rho_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    # Lower gas density at the convection section
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    rho_Ts_LB = 2116.22045 * 27.777276 / (778.169 * 1.985 * Ts_UB)
    return rho_Ts_LB


# the mean density of the gas in the convection section
def HEATER_rho_conv_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max)
    rho_conv_LB = 2116.22045 * 27.777276 / (778.169 * 1.985 * ((Ts_UB +Tfb_UB)/2))
    return rho_conv_LB

def HEATER_rho_conv_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    Ts_LB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    rho_conv_UB = 2116.22045 * 27.777276 / (778.169 * 1.985 * ((Ts_LB + Tfb_LB)/2))
    return rho_conv_UB


# the mean temperature of stack
def HEATER_Tmean_stack(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    Ts_LB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)

    # 만약 Ts_LB와 Ts_UB가 리스트 또는 numpy array 형태로 반환된다면,
    Ts_LB = np.array(Ts_LB)
    Ts_UB = np.array(Ts_UB)
    # 0보다 큰 값들만 필터링하여 각각 최소값을 구합니다.
    valid_Ts_LB = Ts_LB[Ts_LB > 0]
    valid_Ts_UB = Ts_UB[Ts_UB > 0]

    if valid_Ts_LB.size > 0 and valid_Ts_UB.size > 0:
        min_Ts_LB = np.min(valid_Ts_LB)
        min_Ts_UB = np.min(valid_Ts_UB)
        Ts_mean = (min_Ts_LB + min_Ts_UB) / 2.0
    else:
        Ts_mean = Tfb_LB  # 또는 적절한 기본값 할당

    Tmean_delta = 104
    Tmean_stack = (2 * Ts_mean - Tmean_delta)/2

    return Tmean_stack


# the mean density of the gas along the stack (temperature variation = 40C = 104F)
def HEATER_rho_stack(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max):
    Tmean_stack = HEATER_Tmean_stack(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)

    rho_stack = 2116.22045 * 27.777276 / (778.169 * 1.985 * Tmean_stack)
    return rho_stack
