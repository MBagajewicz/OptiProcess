###################################################################################################################
#region Titles and Header
# Nature: Reflux Drum model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          06-Mar-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Reflux Drum Sizing
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
from Reflux_Drum.Calculations import Calculations_Reflux_Drum_Diameter

#endregion
##################################################################################################################

##################################################################################################################
#region Calculations


# Vapor height (m)
def fun_hV(Di):
    hV = np.maximum(0.3, 0.2 * Di) # hV >= 0.3m, hv>= 20%D 
    return hV

# Liquid height (m)
def fun_hL(D):
    Di = Calculations_Reflux_Drum_Diameter.fun_Di(D)
    hV = fun_hV(Di)
    hL = Di - hV - 0.3
    return hL

##################################################################################################################
#endregion