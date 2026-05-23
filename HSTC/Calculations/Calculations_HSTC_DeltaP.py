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
    Calculations_HSTC_Shell_Flow,
    Calculations_HSTC_Tube_Flow
)
from math import pi
import numpy as np
#endregion

#region Calculations

def fun_ft(Ret):
    ft = 0.014 + 1.056/Ret**0.42
    return ft

def fun_fs(Res):
    fs = 1.728/Res**0.188
    return fs

# F factor for Darcy–Weisbach equation
def fun_KDW(Npt):
    K = 1.6 * np.ones(Npt.shape)
    if isinstance(Npt,float) or isinstance(Npt,int):
        if Npt == 1: K = 0.9
    else:
        K[Npt == 1] = 0.9
    return K

def fun_dPt(Ds, dte, Npt, rp, lay, L, mt, rot, mit, thk, Fsc):
    # Tube-side pressure drop
    vt = Calculations_HSTC_Tube_Flow.fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc)
    Ret = Calculations_HSTC_Tube_Flow.fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc)
    ft = fun_ft(Ret)
    K = fun_KDW(Npt)
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
    dPt = (rot*ft*Npt*L*vt**2)/(2*dti) + rot*K*Npt*vt**2/2
    return dPt

def fun_dPs(Ds, dte, rp, lay, L, Nb, ms, ros, mis):
    KDeq = Calculations_HSTC_Geometry.fun_KDeq(lay)
    ltp = Calculations_HSTC_Geometry.fun_ltp(rp, dte)
    Deq = Calculations_HSTC_Geometry.fun_Deq(KDeq,ltp,dte)
    vs = Calculations_HSTC_Shell_Flow.fun_vs(Ds, rp, L, Nb, ms, ros)
    Res = Calculations_HSTC_Shell_Flow.fun_Res(Ds, dte, rp, lay, L, Nb, ms, ros, mis)
    fs = fun_fs(Res)
    dPs = (ros*fs*Ds*(Nb + 1)*vs**2)/(2*Deq)
    return dPs

def fun_dPs_corr(dPs):
    dPs_two_phase = 0.5*dPs
    return dPs_two_phase

#endregion