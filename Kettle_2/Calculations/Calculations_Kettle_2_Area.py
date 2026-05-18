###################################################################################################################
#region Titles and Header
# Nature: Kettle model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          19-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle Area model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from Kettle_2.Calculations import Calculations_Kettle_2_Geometry
from math import pi
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Heat exchanger external area
def fun_A(Ds, dte, Npt, rp, lay, L):
    # Heat exchanger area
    Ntt = Calculations_Kettle_2_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay)
    A = Ntt*pi*dte*L
    return A

#endregion