##################################################################################################################
#region Titles and Header
# Nature: Cost functions
# Methodology: Set trimming + Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Nov-2024     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Cost calculation related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from Reflux_Drum.Calculations import Calculations_Reflux_Drum_Diameter
from math import pi
#endregion
##################################################################################################################

##################################################################################################################
#region Calculations=

def Towler_and_Sinnot_Cost_Function(a,b,n,S):

    CAPEX = a + b*S**n

    return CAPEX

def fun_CAPEX(Wshell): # Wshell must be in kg

    CAPEX = Towler_and_Sinnot_Cost_Function(10200, 31, 0.85, Wshell)

    return CAPEX


# Mass of the vessel (kg)
def f_Wshell(D,L,roshell):          
    twall = Calculations_Reflux_Drum_Diameter.f_twall(D)
    Wshell = pi*roshell*D*L*twall
    return Wshell

#endregion
##################################################################################################################
