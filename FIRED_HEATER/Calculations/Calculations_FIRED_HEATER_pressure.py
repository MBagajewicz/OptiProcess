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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_boxsize, Calculations_FIRED_HEATER_oil_velocity, Calculations_FIRED_HEATER_tubes
#endregion


#region Calculations

def HEATER_Reoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil):
    # Re for oil in each tube
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)
    Voil_Tube = Calculations_FIRED_HEATER_oil_velocity.HEATER_Voil_Tube(Do, Moil, Npasses, rho_oil)
    Reoil_Tube = Di_Tube * Voil_Tube * rho_oil / mu_oil
    return Reoil_Tube

def HEATER_Fric_Tube(Do, Moil, Npasses, rho_oil, mu_oil):
    # Darcy friction factor
    Reoil_Tube = HEATER_Reoil_Tube(Do, Moil, Npasses, rho_oil, mu_oil)
    Fric_Tube = 0.0055 *( 1 + ((20000*(0.0001476/Do)) + 1000000/Reoil_Tube)**(1/3))
    return Fric_Tube

def HEATER_L_oil(L, pk1, Npconv, Npasses, Nprad, Ntceil, Nrconv ):
    # length of the oil tube
    El = Calculations_FIRED_HEATER_boxsize.HEATER_El(L, pk1)
    Ntshield = Calculations_FIRED_HEATER_tubes.HEATER_Ntshield(Npconv, Npasses)
    Ntwall = Calculations_FIRED_HEATER_tubes.HEATER_Ntwall(Nprad, Npasses, Ntceil)
    L_oil = El*( Ntshield * (Nrconv+1) + Ntwall + Ntceil )
    return L_oil

def HEATER_PDrop_Tube(Do, Moil, Npasses, rho_oil, mu_oil, L, pk1, Npconv, Nprad, Ntceil, Nrconv ):
    # pressure drop in oil tube
    Fric_Tube = HEATER_Fric_Tube(Do, Moil, Npasses, rho_oil, mu_oil)
    L_oil = HEATER_L_oil(L, pk1, Npconv, Npasses, Nprad, Ntceil, Nrconv )
    Di_Tube = Calculations_FIRED_HEATER_tubes.HEATER_Di_Tube(Do)
    Voil_Tube = Calculations_FIRED_HEATER_oil_velocity.HEATER_Voil_Tube(Do, Moil, Npasses, rho_oil)
    PDrop_Tube = (Fric_Tube/32.2)*(L_oil/Di_Tube)*(rho_oil*(np.power(Voil_Tube,2))/2)
    return PDrop_Tube