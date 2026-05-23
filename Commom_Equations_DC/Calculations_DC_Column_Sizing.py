###################################################################################################################
#region Titles and Header
# Nature: Distillation Column 
# Methodology: Set trimming + Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          06-Mar-2024     Alice Peccini             Proposed 
#   0.1          28-Jan-2026     Alice Peccini             Correction on twall calculation
##################################################################################################################
# INPUT: Heat exchanger related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from math import pi
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Calculations

# Height of the column (m)
def f_Hc(lt, Nt):
    Hc = Nt*lt
    #print('Hc',Hc)
    return Hc

# Column wall thicknes (m) 
def f_twall(Dc):
    if isinstance(Dc,float) or isinstance(Dc,int):
        if Dc > 3: twall = 0.012
        elif Dc > 2.5: twall = 0.010
        elif Dc > 2: twall = 0.009
        elif Dc > 1: twall = 0.007
        else: twall = 0.005
    else:
        twall = 0.005*np.ones(Dc.shape)
        twall[Dc > 1] = 0.007
        twall[Dc > 2] = 0.009
        twall[Dc > 2.5] = 0.010
        twall[Dc > 3] = 0.012
    return twall

# Mass of the column shell (kg)
def f_Wshell(lt, Nt, Dc, roshell):          
    Hc = f_Hc(lt,Nt)
    twall = f_twall(Dc)
    Wshell = pi*roshell*Dc*Hc*twall
    return Wshell

# Column Diameter - Lowenstein(1961) - from Towler and Sinnot 2nd ed. pg. 853
def f_Diameter(lt, rhol, rhov, Vmax):

    max_velocity = ( - 0.171*lt**2 + 0.27*lt - 0.047)*((rhol - rhov)/rhov)**0.5
    Dc = (4*Vmax/(pi*rhov*max_velocity))

    return Dc

#endregion
##################################################################################################################
