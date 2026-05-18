###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Entrainment Model
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray - Entrainment related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from STRAY.Calculations import Calculations_STRAY_Flooding
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=
# % of flooding (Fflood) defined by vapor flow velocity (un = f(lw, Dc, Vw, rov)) and flooding velocity (uflood = f((lw, Dc, wczin, wczout, dh, lp, lay, Lw, Vw, rol, rov, lt, sig)))
def f_Fflood(lw, Dc, Vw, rov, wczin, wczout, dh, lp, lay, Lw, rol, lt, sig):
    un = Calculations_STRAY_Flooding.f_un(lw, Dc, Vw, rov)
    uflood = Calculations_STRAY_Flooding.f_uflood(lw, Dc, wczin, wczout, dh, lp, lay, Lw, Vw, rol, rov, lt, sig)
    Fflood = un/uflood
    #print('Fflood',Fflood)
    return Fflood

# Fractional entrainment (Psi), defined by % of flooding (Fflood = f(lw, Dc, Vw, rov, wczin, wczout, dh, lp, lay, Lw, rol, rov, lt, sig)) and liquid vapor flow factor (Flv = f((Lw, Vw, rol, rov)))
def f_Psi(lw, Dc, Vw, rov, wczin, wczout, dh, lp, lay, Lw, rol, lt, sig):
    Fflood = f_Fflood(lw, Dc, Vw, rov, wczin, wczout, dh, lp, lay, Lw, rol, lt, sig)
    Flv = Calculations_STRAY_Flooding.f_Flv(Lw, Vw, rol, rov)
    Psi = np.exp(-7.9196 + 1.0891*Fflood - (0.0705 + 2.1916*Fflood)*np.log(Flv) + (0.046 - 0.605*Fflood + 1.2669*Fflood**2 - 0.9563*Fflood**3)*(np.log(Flv)**2))
    #print('Psi',Psi)
    return Psi
