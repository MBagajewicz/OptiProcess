###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Column Size Calculation
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          21-may-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Column diameter transition
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
from math import pi
from Commom_Equations_DC import Calculations_DC_Column_Sizing
#endregion
##################################################################################################################

##################################################################################################################
#region Calculations=

# Transition mass
def f_Wshell_trans(DSTRIP, DRECT, roshell):  
    Atrans = pi*abs(DSTRIP**2 - DRECT**2)/2
    twall = Calculations_DC_Column_Sizing.f_twall(np.maximum(DRECT,DSTRIP))
    Wshell = roshell*twall*Atrans
    return Wshell