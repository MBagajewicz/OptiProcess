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
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_boxsize
#endregion


#region Calculations

# Draft produced by the density difference between the atmospheric air and the gas
def HEATER_Draft(Tflame, Hs, Do, Nprad, Npasses, Ntceil, Rpr, lf, Rpv, Nrconv):
    Gravity = 32.2
    rho_ambient = 0.07647425
    rho_burner =  2116.22045 * 27.777276 / (778.169 * 1.985 * Tflame)
    Htotal = Calculations_FIRED_HEATER_boxsize.HEATER_Htotal(Hs, Do, Nprad, Npasses, Ntceil, Rpr, lf, Rpv, Nrconv)
 
    Draft = Gravity * (rho_ambient - rho_burner) * Htotal
    return Draft



