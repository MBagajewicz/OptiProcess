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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_area_flow, Calculations_FIRED_HEATER_boxsize, Calculations_FIRED_HEATER_friction_factor, Calculations_FIRED_HEATER_gas_density, Calculations_FIRED_HEATER_gas_flow, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

# 1. pressure drop across the finned horizontal tubes in the convection section 
def HEATER_Beta(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf):
    As = Calculations_FIRED_HEATER_area_flow.HEATER_As(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf)
    Wconv = Calculations_FIRED_HEATER_boxsize.HEATER_Wconv(Npconv, Npasses, lf, Do, Rph)
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Beta = As / (Wconv*El)
    return Beta

def HEATER_ahpha_stack(lf, Rph, Nf, tf, Nrconv, Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    rho_conv_LB = Calculations_FIRED_HEATER_gas_density.HEATER_rho_conv_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    rho_Tfb_UB = Calculations_FIRED_HEATER_gas_density.HEATER_rho_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)
    rho_Ts_LB = Calculations_FIRED_HEATER_gas_density.HEATER_rho_Ts_LB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Beta = HEATER_Beta(L, pk1, Npconv, Npasses, lf, Do, Rph, Nf, tf)
    alpha_stack = rho_conv_LB * (1/rho_Tfb_UB - 1/rho_Ts_LB)*(1 + np.power(Beta,2))/(4*Nrconv)
    return alpha_stack


def HEATER_DPfin_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv, Nrconv, Flux_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    f_factor_LB = Calculations_FIRED_HEATER_friction_factor.HEATER_f_factor_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv)
    alpha_stack = HEATER_ahpha_stack(lf, Rph, Nf, tf, Nrconv, Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Flux_Max, Tfb_Max, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)
    Ggas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_LB(L, pk1, Nprad, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, Npconv, Npasses, lf, Rph, Nf, tf)
    rho_conv_UB = Calculations_FIRED_HEATER_gas_density.HEATER_rho_conv_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Max)

    DPfin_LB = (f_factor_LB + alpha_stack) * Nrconv * np.power(Ggas_LB,2) / rho_conv_UB
    return DPfin_LB



# 2. pressure drop across the shield tubes
def HEATER_As_shield(L, pk1, Npconv, Npasses, lf, Do, Rph):
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Wconv = Calculations_FIRED_HEATER_boxsize.HEATER_Wconv(Npconv, Npasses, lf, Do, Rph)
    Ntshield = Calculations_FIRED_HEATER_tubes.HEATER_Ntshield(Npconv, Npasses)

    As_shield = El * ( Wconv - Ntshield *Do)
    return As_shield

def HEATER_Gshield_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, lf, Rph):
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min)
    As_shield = HEATER_As_shield(L, pk1, Npconv, Npasses, lf, Do, Rph)
    Gshield_LB = Mgas_LB / As_shield
    return Gshield_LB


def HEATER_DPshield_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, lf, Rph, Flux_Max):
    Gshield_LB = HEATER_Gshield_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, lf, Rph)
    rho_Tfb_UB = Calculations_FIRED_HEATER_gas_density.HEATER_rho_Tfb_UB(Tflame, L, pk1, Nprad, Npconv, Npasses, Do, Flux_Max, percent_loss_Rad, Flux_Min, Tfb_Min)

    DPshield_LB = 0.2 * np.power(Gshield_LB,2) / (2 * rho_Tfb_UB)
    return DPshield_LB



# 3. Obtain the pressure drop in the convection section
def HEATER_DPconv_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv, Nrconv, Flux_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min):
    DPshield_LB = HEATER_DPshield_LB(L, pk1, Nprad, Npconv, Npasses, Do, Flux_Min, percent_loss_Rad, Tflame, Tfb_Min, lf, Rph, Flux_Max)
    DPfin_LB = HEATER_DPfin_LB(L, pk1, Nprad, Do, Flux_Max, percent_loss_Rad, Tflame, Tfb_Max, Npconv, Npasses, lf, Rph, Nf, tf, mu_gas, Rpv, Nrconv, Flux_Min, hflame, percent_loss_Conv, Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3, Tfb_Min)

    DPconv_LB = DPshield_LB + DPfin_LB
    return DPconv_LB



