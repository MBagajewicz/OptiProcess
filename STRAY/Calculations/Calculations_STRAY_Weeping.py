###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Weeping Model
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray - Weeping related functions
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
from STRAY.Calculations import Calculations_STRAY_Geometry
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=

# Flow velocity throughout the tray holes (uh) defined by hole area (Ah = f(lw, Dc, wczin, wczout, dh, lp, lay)), vapor mass flow rate (Vw) and vapor specific mass (rov):
def f_uh(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov):
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, wczin, wczout, dh, lp, lay)
    uh = Vw/(rov*Ah)
    #print('uh',uh)
    return uh

# Height of the liquid crest over the weir (how) defined by weir length (lw), liquid mass flow rate (Lw) and loquid specific mass (rol):
def f_how(lw, Lw, rol):
    how = 750*0.001*(Lw/(rol*lw))**(2/3)
    #print('how',how)
    return how

# Constant of weeping correlation (K2) defined by height of the liquid crest over the weir (how = f(lw, Lw, rol)) and weirh height (hw):
def f_K2(lw, Lw, rol, hw):
    how = f_how(lw, Lw, rol)
    K2 = 23.48 + 1.66*np.log(1000*(hw + how))
    #print('K2',K2)
    return K2

# Minimum vapor flow velocity (uhmin) defined by constant of weeping correlation (K2 = f(lw, Lw, rol, hw)), hole diameter (dh), and vapor specific mass (rov):
def f_uhmin(lw, Lw, rol, hw, dh, rov):
    K2 = f_K2(lw, Lw, rol, hw)
    uhmin = (K2 - 0.9*(25.4 - 1000*dh))/(rov)**(1/2)
    #print('uhmin',uhmin)
    return uhmin

