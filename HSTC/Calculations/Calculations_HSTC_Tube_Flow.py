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
def fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc):
    # Tube-side velocity
    qt = mt/rot
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_HSTC_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay, Fsc)
    Ntp = np.round(Ntt/Npt)
    vt = (qt/Ntp)/(pi*dti**2/4)
    return vt

def fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc):
    # Tube-side Reynolds number
    vt = fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc)
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
    Ret = (dti*vt*rot)/mit
    return Ret

def fun_Nut(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Prt, Fsc):
    # Tube-side Nusselt number
    Ret = fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc)
    Nut = 0.024*Ret**0.8*Prt**0.4
    return Nut



#endregion
