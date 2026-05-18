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

#endregion
##################################################################################################################

##################################################################################################################
#region Calculations

# Column wall thicknes (m) 
def f_twall(D):
    if isinstance(D,float) or isinstance(D,int):
        twall = 0.005
        if D > 1: twall = 0.007
        elif D > 2: twall = 0.009
        elif D > 2.5: twall = 0.010
        elif D > 3: twall = 0.012
    else:
        twall = 0.005*np.ones(D.shape)
        twall[D > 1] = 0.007
        twall[D > 2] = 0.009
        twall[D > 2.5] = 0.010
        twall[D > 3] = 0.012
    return twall

# Internal diameter (m)
def fun_Di(D):
    twall = f_twall(D)
    Di = D - 2*twall
    return Di


##################################################################################################################
#endregion