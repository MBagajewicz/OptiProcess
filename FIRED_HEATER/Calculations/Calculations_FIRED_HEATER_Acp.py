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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_tubes, Calculations_FIRED_HEATER_Aot, Calculations_FIRED_HEATER_boxsize
#endregion


#region Calculations

def HEATER_Acp_shield(Npconv, Npasses, Do, Rpr, L, pk1):
    # convective heat transfer area
    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Ntshield = Calculations_FIRED_HEATER_tubes.HEATER_Ntshield(Npconv, Npasses)
    Acp_shield = El * Ntshield * dcr
    return Acp_shield


def HEATER_Acp_wall(L, pk1, Nprad, Npconv, Npasses, Do, Rpr):
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Ntrad = Calculations_FIRED_HEATER_tubes.HEATER_Ntrad(Nprad, Npconv, Npasses)
    Ntshield = Calculations_FIRED_HEATER_tubes.HEATER_Ntshield(Npconv, Npasses)
    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)

    Acp_wall = El*(Ntrad-Ntshield)*dcr
    return Acp_wall

def HEATER_Acp(L, pk1, Nprad, Npconv, Npasses, Do, Rpr):
    Acp_shield = HEATER_Acp_shield(Npconv, Npasses, Do, Rpr, L, pk1)
    Acp_wall = HEATER_Acp_wall(L, pk1, Nprad, Npconv, Npasses, Do, Rpr)

    Acp = Acp_shield + Acp_wall
    return Acp

def HEATER_PartPres_CO2_H2O(excess_air):
    PartPres_CO2_H2O = (2/3)* (0.29067-0.0029654*excess_air +2.72e-5 * np.power(excess_air,2)-1.175e-7*np.power(excess_air,3))
    return PartPres_CO2_H2O

def HEATER_Factor_PL(excess_air, L, pk1, Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph, Nprad):
    PartPres_CO2_H2O = HEATER_PartPres_CO2_H2O(excess_air)
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph )
    Hrad = Calculations_FIRED_HEATER_boxsize.HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)

    Factor_PL = PartPres_CO2_H2O *np.power( El * Wrad * Hrad, 1/3 )
    return Factor_PL

def HEATER_alpha(Do, Rpr):
    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)
    
    alpha = 1.2554 - 0.205358 * dcr/Do + 0.00991667 * np.power(dcr/Do,2)
    return alpha

def HEATER_A(L, pk1, Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph, Nprad):
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph )
    Hrad = Calculations_FIRED_HEATER_boxsize.HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)

    A = 2 * Wrad*Hrad + 2 * El*(Wrad +Hrad)
    return A




