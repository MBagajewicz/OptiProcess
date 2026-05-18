###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Column Size Calculation
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray -Residence Time related functions
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
#region Sieve_Tray_Aline=

# Mean Diameter of the column
def f_Dm(Dc):          
    twall = Calculations_DC_Column_Sizing.f_twall(Dc)
    Dm = Dc + twall
    return Dm

# Mass of the column
def f_WColumn(Cw,roshell,Dc,lt,Nt):   
    Dm = f_Dm(Dc)       
    Hc = Calculations_DC_Column_Sizing.f_Hc(lt, Nt)
    twall = Calculations_DC_Column_Sizing.f_twall(Dc)
    WColumn = Cw*pi*roshell*Dm*(Hc + 0.8*Dm)*twall
    return WColumn
