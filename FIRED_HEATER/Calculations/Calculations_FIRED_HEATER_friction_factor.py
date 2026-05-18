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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_clearance, Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_pressure, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_C2(Do, Moil, Npasses, rho_oil, mu_oil):
    Reoil_Tube = Calculations_FIRED_HEATER_pressure.HEATER_Reoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil)
    C2 = 0.075 + 1.85 * np.power(Reoil_Tube,-0.3)
    return C2

def HEATER_C2_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas):
    Ggas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_UB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf)
    C2_LB = 0.075 + 1.85 * np.power(Do * Ggas_UB/mu_gas,-0.3)
    return C2_LB

def HEATER_m(Nf, tf, lf):
    S = Calculations_FIRED_HEATER_clearance.HEATER_S(Nf, tf)
    m = -0.7 * np.power(lf/S, 0.2)
    return m

def HEATER_C4(Do, Rph, Nf, tf, Lf):
    dch = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)
    m = HEATER_m(Nf, tf, Lf)
    C4 = 0.11 * np.power(0.05 * dch/Do, m)
    return C4

def HEATER_C6(Do, Rpv, Rph, Nf):
    dcv = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rpv)
    dch = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)

    C6a = (1.8 - 2.1* np.exp(-0.15*np.power(Nf,2))) * np.exp(-2*dcv/dch)
    C6b = (0.7 - 0.8* np.exp(-0.15*np.power(Nf,2))) * np.exp(-0.6*dcv/dch)
    C6  = 1.11 + C6a - C6b
    return C6


def HEATER_f_factor(Do, Moil, Npasses, rho_oil, mu_oil, Rpv, Rph, Nf, tf, lf):
    C2 = HEATER_C2(Do, Moil, Npasses, rho_oil, mu_oil)
    C4 = HEATER_C4(Do, Rph, Nf, tf, lf)
    C6 = HEATER_C6(Do, Rpv, Rph, Nf)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)

    f_factor = C2 * C4 * C6 * (df/Do)
    return f_factor

def HEATER_f_factor_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv):
    C2_LB = HEATER_C2_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas)
    C4 = HEATER_C4(Do, Rph, Nf, tf, lf)
    C6 = HEATER_C6(Do, Rpv, Rph, Nf)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)

    f_factor_LB = C2_LB * C4 * C6 * (df/Do)
    return f_factor_LB 
