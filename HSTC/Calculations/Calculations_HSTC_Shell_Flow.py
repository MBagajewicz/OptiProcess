###################################################################################################################
#region Titles and Header
# Nature: Horizontal Shell and Tube Condenser model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          20-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle Area model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################


#region Import Library
from HSTC.Calculations import Calculations_HSTC_Geometry
from math import pi
import numpy as np
#endregion

#region Calculations

def fun_vs(Ds, rp, L, Nb, ms, ros):
    qs = ms/ros
    FAR = 1 - 1 / rp
    lbc = (L/(Nb + 1))
    Ar = Ds*FAR*lbc
    vs = qs/Ar
    return vs

def fun_Res(Ds, dte, rp, lay, L, Nb, ms, ros, mis):
    vs = fun_vs(Ds, rp, L, Nb, ms, ros)
    KDeq = Calculations_HSTC_Geometry.fun_KDeq(lay)
    ltp = Calculations_HSTC_Geometry.fun_ltp(rp,dte)
    Deq = Calculations_HSTC_Geometry.fun_Deq(KDeq,ltp,dte)
    Res = (Deq*vs*ros)/mis
    return Res

#endregion
