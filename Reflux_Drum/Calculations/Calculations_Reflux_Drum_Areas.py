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
from math import pi
from Reflux_Drum.Calculations import (
    Calculations_Reflux_Drum_Diameter,
    Calculations_Reflux_Drum_Heights
)

#endregion
##################################################################################################################

##################################################################################################################
#region Calculations

# Total Cross-sectional area (m²)
def fun_A_CS(Di):
    A_CS = pi*Di**2/4
    return A_CS

# Cross-sectional area for liquid control volume (m²)
def fun_A_CS_L_req(L,VC_L):
    A_CS_L_req = VC_L/L
    return A_CS_L_req

# Circle Segment Area (m²)
def fun_A_seg(h,Di):
    Ri = Di/2
    theta = 1 - h/Ri  
    area = Ri**2*np.arccos(theta) - (Ri - h)*np.sqrt(2*h*Ri - h**2)
    return area

# Cross-sectional area for liquid volume below low level (m²)
def fun_A_CS_LL(D, h_LL):
    Di = Calculations_Reflux_Drum_Diameter.fun_Di(D)
    A_CS_LL = fun_A_seg(h_LL, Di)
    return A_CS_LL

# Cross-sectional area for liquid control volume (m²)
def fun_A_CS_L(D):
    Di = Calculations_Reflux_Drum_Diameter.fun_Di(D)
    hV = Calculations_Reflux_Drum_Heights.fun_hV(Di)
    A_CS_V = fun_A_seg(hV,Di)   # Cross-sectional area above HL
    A_CS_LL = fun_A_seg(0.3,Di) # Cross-sectional area below LL
    A_CS = fun_A_CS(Di)         # Total cross-sectional area
    A_CS_L = A_CS - A_CS_V - A_CS_LL
    return A_CS_L


##################################################################################################################
#endregion