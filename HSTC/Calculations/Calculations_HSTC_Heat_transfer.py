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
from HSTC.Calculations import (
    Calculations_HSTC_Geometry,
    Calculations_HSTC_Tube_Flow
) 
import numpy as np
#endregion

#region Calculations

def fun_ht(Ds, dte, Npt, rp, lay, mt, rot, mit, kt, thk, Prt, Fsc):
    Nut = Calculations_HSTC_Tube_Flow.fun_Nut(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Prt, Fsc)
    dti = Calculations_HSTC_Geometry.fun_dti(dte, thk)
    ht = Nut*kt/dti
    return ht

def fun_hs(Ds, dte, Npt, rp, lay, L, ros, rovs, ks, ms, mis, Fsc):
    Ntt = Calculations_HSTC_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay, Fsc)
    hs = 0.954*(ros*(ros - rovs)*9.81*ks**3*L/(ms*mis))**(1/3)*Ntt**(2/9)
    return hs

def fun_U(Ds, dte, Npt, rp, lay, L, mt, rot, mit, kt, Rft, ms, ros, rovs, mis, ks, Rfs, thk, ktube, Prt, Fsc):
    dti = Calculations_HSTC_Geometry.fun_dti(dte, thk)
    ht = fun_ht(Ds, dte, Npt, rp, lay, mt, rot, mit, kt, thk, Prt, Fsc)
    hs = fun_hs(Ds, dte, Npt, rp, lay, L, ros, rovs, ks, ms, mis, Fsc)
    U = 1 / (1/ht*(dte/dti) + Rft*(dte/dti) + dte * np.log(dte/dti)/(2*ktube) + Rfs + 1/hs)
    return U

def fun_A_req(U, Q, dTLM):
    A_req = Q/(U*dTLM)
    return A_req

#endregion