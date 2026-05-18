###################################################################################################################
#region Titles and Header
# Nature: Kettle model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          19-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle tube-side model  
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
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Tube side velocity
def fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk):
    qt = mt/rot
    dti = Calculations_Kettle_2_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_Kettle_2_Geometry.fun_Ntt(Ds,dte,Npt,rp,lay)
    Ntp = Ntt/Npt
    vt = (qt/Ntp)/(pi*dti**2/4)
    return vt

# Tube side Reynolds number
def fun_Ret(dte, rot, mit, thk, vt):
    dti = Calculations_Kettle_2_Geometry.fun_dti(dte,thk)
    Ret = (dti*vt*rot)/mit
    return Ret

# Friction factor
def fun_f(Ret):
    ft = 0.014 + 1.056/(Ret**0.42)
    return ft

# F factor for Darcy–Weisbach equation
def fun_KDW(Npt):
    K = 1.6 * np.ones(Npt.shape)
    K[Npt == 1] = 0.9
    return K

# Tube side pressure drop
def fun_dPt(Ds, dte, Npt, rp, lay, L, mt, rot, mit, thk):
    vt = fun_vt(Ds, dte, Npt, rp, lay, mt, rot, thk)
    Ret = fun_Ret(dte, rot, mit, thk, vt)
    ft = fun_f(Ret)
    K = fun_KDW(Npt)
    dti = Calculations_Kettle_2_Geometry.fun_dti(dte,thk)
    dPt = (rot*ft*Npt*L*vt**2)/(2*dti) + rot*K*Npt*vt**2/2
    return dPt

# Two phase correction for pressure drop on the tube side
def fun_dPt_corr(dPt):
    dPt_two_phases = 0.5*dPt
    return dPt_two_phases

#endregion