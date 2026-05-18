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
from Hor_ST_Cond.Calculations import (
    Calculations_Hor_ST_Cond_Geometry,
    Calculations_Hor_ST_Cond_Shell_Flow,
    Calculations_Hor_ST_Cond_Tube_Flow
=======
from HSTC.Calculations import (
    Calculations_HSTC_Geometry,
    Calculations_HSTC_Shell_Flow,
    Calculations_HSTC_Tube_Flow
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    vt = Calculations_Hor_ST_Cond_Tube_Flow.fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc)
    Ret = Calculations_Hor_ST_Cond_Tube_Flow.fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc)
    ft = fun_ft(Ret)
    K = fun_KDW(Npt)
    dti = Calculations_Hor_ST_Cond_Geometry.fun_dti(dte,thk)
=======
    vt = Calculations_HSTC_Tube_Flow.fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk, Fsc)
    Ret = Calculations_HSTC_Tube_Flow.fun_Ret(Ds, dte, Npt, rp, lay, mt, rot, mit, thk, Fsc)
    ft = fun_ft(Ret)
    K = fun_KDW(Npt)
    dti = Calculations_HSTC_Geometry.fun_dti(dte,thk)
>>>>>>> Stashed changes
    dPt = (rot*ft*Npt*L*vt**2)/(2*dti) + rot*K*Npt*vt**2/2
    return dPt

def fun_dPs(Ds, dte, rp, lay, L, Nb, ms, ros, mis):
<<<<<<< Updated upstream
    KDeq = Calculations_Hor_ST_Cond_Geometry.fun_KDeq(lay)
    ltp = Calculations_Hor_ST_Cond_Geometry.fun_ltp(rp, dte)
    Deq = Calculations_Hor_ST_Cond_Geometry.fun_Deq(KDeq,ltp,dte)
    vs = Calculations_Hor_ST_Cond_Shell_Flow.fun_vs(Ds, rp, L, Nb, ms, ros)
    Res = Calculations_Hor_ST_Cond_Shell_Flow.fun_Res(Ds, dte, rp, lay, L, Nb, ms, ros, mis)
=======
    KDeq = Calculations_HSTC_Geometry.fun_KDeq(lay)
    ltp = Calculations_HSTC_Geometry.fun_ltp(rp, dte)
    Deq = Calculations_HSTC_Geometry.fun_Deq(KDeq,ltp,dte)
    vs = Calculations_HSTC_Shell_Flow.fun_vs(Ds, rp, L, Nb, ms, ros)
    Res = Calculations_HSTC_Shell_Flow.fun_Res(Ds, dte, rp, lay, L, Nb, ms, ros, mis)
>>>>>>> Stashed changes
    fs = fun_fs(Res)
    dPs = (ros*fs*Ds*(Nb + 1)*vs**2)/(2*Deq)
    return dPs

def fun_dPs_corr(dPs):
    dPs_two_phase = 0.5*dPs
    return dPs_two_phase

#endregion