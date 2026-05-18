###################################################################################################################
#region Titles and Header
# Nature: Horizontal Shell and Tube Condenser model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
<<<<<<< Updated upstream
#   0.0          20-Fev-2025     Alice Peccini              Proposed 
#   0.1          03-Jun-2025     Miguel Bagajewicz          Extension to Intensified Condenser+Desuperheater+Multic
=======
#   0.0        20-Fev-2025     Alice Peccini                 Proposed 
#   0.1        03-Jun-2025     Miguel Bagajewicz             First Set up to add Inntensification/Desuperheating 
#                                                            and Multicomponent Condensation
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
from Hor_ST_Cond.Calculations import Calculations_Hor_ST_Cond_Geometry
=======
from HSTC.Calculations import Calculations_HSTC_Geometry
>>>>>>> Stashed changes
from math import pi
import numpy as np
#endregion

#region Calculations
def fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc):
    # Tube-side velocity
    qt = mt/rot
<<<<<<< Updated upstream
    dti = Calculations_Hor_ST_Cond_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_Hor_ST_Cond_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay, Fsc)
=======
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_HSTC_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay, Fsc)
>>>>>>> Stashed changes
    Ntp = np.round(Ntt/Npt)
    vt = (qt/Ntp)/(pi*dti**2/4)
    return vt

def fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc):
    # Tube-side Reynolds number
    vt = fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc)
<<<<<<< Updated upstream
    dti = Calculations_Hor_ST_Cond_Geometry.fun_dti(dte,thk)
=======
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
>>>>>>> Stashed changes
    Ret = (dti*vt*rot)/mit
    return Ret

def fun_Nut(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Prt, Fsc):
    # Tube-side Nusselt number
    Ret = fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc)
    Nut = 0.024*Ret**0.8*Prt**0.4
    return Nut



#endregion
